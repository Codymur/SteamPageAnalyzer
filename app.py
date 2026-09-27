import streamlit as st
from scraper import scrape_steam_page
from ai_analyzer import generate_page_feedback

# Page Configuration
st.set_page_config(
    page_title="Steam Page Estimator & AI Auditor",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def analyze_steam_page(url: str) -> dict:
    """Fetches data from the scraper and calculates revenue/owner estimates."""
    scraped_data = scrape_steam_page(url)
    
    if scraped_data.get("error"):
        st.error(scraped_data["error"])
        st.stop()
        
    actual_reviews = scraped_data.get("reviews", 0)
    actual_price = scraped_data.get("price", 0.0)
    title = scraped_data.get("title", "Unknown Title")
    description = scraped_data.get("description", "")
    genres = scraped_data.get("genres", [])
    tags = scraped_data.get("tags", [])
    
    # Boxleiter Method (30x multiplier)
    estimated_owners = actual_reviews * 30
    
    # Hemorrhage Formula (~50% net take-home)
    gross_revenue = estimated_owners * actual_price
    net_revenue = gross_revenue * 0.50
    
    return {
        "title": title,
        "description": description,
        "genres": genres,
        "tags": tags,
        "reviews": actual_reviews,
        "owners": estimated_owners,
        "gross": gross_revenue,
        "net": net_revenue,
        "price": actual_price
    }

# Main Dashboard UI
st.title("📊 Steam Page Estimator & AI Auditor")
st.markdown("Enter a Steam Store URL to estimate total revenue/owners and receive AI-driven conversion recommendations.")

st.write("---")

url_input = st.text_input(
    "Steam Store URL", 
    placeholder="e.g., https://store.steampowered.com/app/123456/Your_Game/"
)
analyze_button = st.button("Run Analysis", type="primary")

# Results Display
if analyze_button and url_input:
    with st.spinner("Scraping Steam API, Community Tags, and running AI audit..."):
        
        results = analyze_steam_page(url_input)
        
        st.success(f"Analysis complete for: {results['title']}")
        
        # Financial & Metric Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Estimated Net Revenue", 
                value=f"${results['net']:,.0f}",
                delta="Take-home after Steam cut & refunds",
                delta_color="off"
            )
            
        with col2:
            st.metric(
                label="Estimated Gross", 
                value=f"${results['gross']:,.0f}"
            )
            
        with col3:
            st.metric(
                label="Estimated Owners", 
                value=f"{results['owners']:,}"
            )
            
        with col4:
            st.metric(
                label="Public Reviews", 
                value=f"{results['reviews']:,}"
            )

        # Mathematical Breakdown
        st.write("---")
        with st.expander("How was this calculated? (The Math)"):
            st.markdown("""
            **The Boxleiter Method**
            * We scraped total public reviews.
            * Applied a baseline **30x review-to-sales multiplier**.
            
            **The Hemorrhage Formula**
            * Gross Revenue = Estimated Owners × USD Price.
            * Net Revenue deducts ~50% across regional pricing adjustments, refunds, and Valve's 30% cut.
            """)

        # AI Optimization Section
        st.subheader("🤖 AI Page Optimization & Market Audit")
        
        audit_col1, audit_col2 = st.columns([1, 2])
        
        with audit_col1:
            st.markdown("**Top Community Tags:**")
            st.write(", ".join(results["tags"][:8]) if results["tags"] else "None found")
            
            st.markdown("**Current Genres:**")
            st.write(", ".join(results["genres"]) if results["genres"] else "None found")
            
            st.markdown("**Current Short Description:**")
            st.info(results["description"] if results["description"] else "No short description found.")
            
        with audit_col2:
            # Generate AI feedback using Groq (Llama 3.3 70B)
            ai_feedback = generate_page_feedback(
                results["title"], 
                results["description"], 
                results["genres"],
                results["tags"]
            )
            st.markdown(ai_feedback)

elif analyze_button and not url_input:
    st.warning("Please enter a valid Steam URL first.")