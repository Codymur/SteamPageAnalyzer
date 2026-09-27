import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def generate_page_feedback(title, description, genres, tags):
    """Passes scraped Steam data and tags to Groq for strict sub-genre benchmark analysis."""
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Error: GROQ_API_KEY not found in .env file."

    try:
        client = Groq(api_key=api_key)
        
        all_models = [m.id for m in client.models.list().data]
        
        preferred_chat_models = [
            "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile",
            "llama3-70b-8192",
            "llama-3.1-8b-instant",
            "llama3-8b-8192",
            "gemma2-9b-it",
            "mixtral-8x7b-32768"
        ]
        
        selected_model = None
        for model_id in preferred_chat_models:
            if model_id in all_models:
                selected_model = model_id
                break
                
        if not selected_model:
            gated_or_specialized = [
                "guard", "embed", "whisper", "bge", "safeguard", 
                "canopylabs", "orpheus", "pascal", "compound"
            ]
            chat_capable = [
                m for m in all_models 
                if not any(x in m.lower() for x in gated_or_specialized)
            ]
            if chat_capable:
                selected_model = chat_capable[0]

        if not selected_model:
            return "Groq Error: No compatible open chat models found for your API key."

        tags_formatted = ', '.join(tags[:10]) if tags else 'None found'

        prompt = f"""You are an expert Steam market researcher specializing in sub-genre target demographics.

Analyze the following Steam page details:
- Title: {title}
- Official Genres: {', '.join(genres)}
- Steam Community User Tags (CRITICAL): {tags_formatted}
- Short Description: {description}

Provide your analysis using EXACTLY the following structure:

### 🎯 Store Page Rating: [Score]/10
[1 sentence rating justification focusing on hook strength, clarity, and sub-genre keyword optimization.]

### 💡 Actionable Conversion Fixes
* **[Fix 1 Title]**: [Brief explanation]
* **[Fix 2 Title]**: [Brief explanation]
* **[Fix 3 Title]**: [Brief explanation]

### 🎮 More Like This (Direct Sub-Genre Competitors)
List 3-4 existing Steam games that belong strictly to the EXACT same sub-genre and target audience as "{title}". 
CRITICAL RULE: Match specific mechanics, game feel, or sub-genres (e.g., if it's a Rogue-lite FPS, deckbuilder, physics puzzle, or precision platformer, only list games in that exact sub-niche). DO NOT suggest generic broad-genre games. For each game, add a 1-line note explaining why it is a direct mechanical/visual benchmark.
"""

        response = client.chat.completions.create(
            model=selected_model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Groq API Error: {e}"