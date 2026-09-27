import re
import requests
from bs4 import BeautifulSoup

def extract_app_id(url: str) -> str:
    """Extracts the numerical App ID from a standard Steam Store URL."""
    match = re.search(r'/app/(\d+)', url)
    return match.group(1) if match else None

def scrape_steam_page(url: str) -> dict:
    """
    Fetches title, price, description, genres, user tags, and review count.
    """
    app_id = extract_app_id(url)
    if not app_id:
        return {"error": "Could not find a valid App ID in the URL."}

    # 1. Fetch metadata via the Storefront API
    api_url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    try:
        api_response = requests.get(api_url, timeout=10).json()
        if not api_response or str(app_id) not in api_response or not api_response[str(app_id)].get("success"):
            return {"error": "Steam API rejected the request or the game does not exist."}
            
        game_data = api_response[str(app_id)]["data"]
        title = game_data.get("name", "Unknown Title")
        short_description = game_data.get("short_description", "")
        
        genres_data = game_data.get("genres", [])
        genres = [genre["description"] for genre in genres_data] if genres_data else []
        
        is_free = game_data.get("is_free", False)
        if is_free:
            price = 0.0
        else:
            price = game_data.get("price_overview", {}).get("final", 0) / 100.0
            
    except Exception as e:
        return {"error": f"Failed to fetch API data: {e}"}

    # 2. Scrape review count AND User Tags via BeautifulSoup
    cookies = {
        'birthtime': '283993201', 
        'lastagecheckage': '1-0-1980', 
        'wants_mature_content': '1'
    }
    
    review_count = 0
    tags = []
    
    try:
        html_response = requests.get(url, cookies=cookies, timeout=10)
        soup = BeautifulSoup(html_response.text, 'html.parser')

        # Scrape Review Count
        meta_review = soup.find('meta', itemprop='reviewCount')
        if meta_review and meta_review.get('content'):
            review_count = int(meta_review['content'])
        else:
            review_summary = soup.find_all('span', class_='responsive_hidden')
            for span in review_summary:
                if 'reviews' in span.text.lower():
                    numbers = re.sub(r'[^\d]', '', span.text)
                    if numbers:
                        review_count = int(numbers)
                        break

        # Scrape Community User Tags (Provides exact sub-genre precision)
        tag_elements = soup.find_all('a', class_='app_tag')
        tags = [t.text.strip() for t in tag_elements if t.text.strip() and t.text.strip() != '+']

    except Exception as e:
        print(f"Warning: Could not scrape HTML details - {e}")

    return {
        "title": title,
        "price": price,
        "description": short_description,
        "genres": genres,
        "tags": tags,
        "reviews": review_count,
        "error": None
    }