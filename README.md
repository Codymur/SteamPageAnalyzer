# 📊 Steam Page Estimator & AI Auditor

A Streamlit app that estimates a Steam game's owner count and revenue from its public store page, then uses Gemini to generate AI-driven suggestions for improving the store page's conversion (wishlists → sales).

## Features

- **Revenue & owner estimation** — pulls live review count and price from Steam, then applies the community-standard **Boxleiter Method** (30x review-to-owner multiplier) and a **Hemorrhage Formula** (~50% net take-home after Steam's cut, refunds, and regional pricing) to estimate gross/net revenue.
- **AI page audit** — sends the game's title, genres, and short description to Gemini, which returns concrete, non-generic suggestions for improving the description's hooks, keywords, and clarity.
- **Simple dashboard UI** — built with Streamlit; enter a store URL, get metrics + AI feedback in one view.

## How it works

1. `scraper.py` extracts the App ID from the URL, fetches title/price/genres/description from Steam's public Storefront API, and fetches the public review count.
2. `app.py` runs the Boxleiter and Hemorrhage math on that data and renders it as metric cards.
3. `ai_analyzer.py` sends the scraped metadata to Gemini and returns three actionable bullet points for improving the page.

## Setup

```bash
git clone <your-repo-url>
cd <repo-folder>
pip install -r requirements.txt
```

Create a `.env` file in the project root with your Gemini API key:

```
GEMINI_API_KEY=your_key_here
```

Get a free key at [Google AI Studio](https://aistudio.google.com/app/apikey).

## Run it

```bash
streamlit run app.py
```

Then paste a Steam store URL, e.g. `https://store.steampowered.com/app/1091500/Cyberpunk_2077/`, and click **Run Analysis**.

## Tech stack

- [Streamlit](https://streamlit.io/) — UI
- [Requests](https://docs.python-requests.org/) + [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) — data fetching
- [Google Gemini API](https://ai.google.dev/) — AI page audit

## ⚠️ Accuracy disclaimer

The 30x multiplier and 50% net-revenue estimate are **rough industry rules of thumb**, not exact figures — actual owner counts and net revenue vary a lot by genre, region, wishlist conversion, and sale history. Treat the numbers here as a ballpark, not ground truth.

## A note on data sourcing

This project reads two kinds of public Steam data:
- Game metadata (title, price, genres, description) via Steam's public Storefront API — the same undocumented-but-widely-used endpoint that sites like SteamDB and IsThereAnyDeal rely on.
- Review counts via Steam's public `appreviews` summary endpoint (no scraping or authentication needed).

Both are read-only, publicly accessible, unauthenticated endpoints, requested at normal single-user rates. That said, Steam's Subscriber Agreement includes a broad clause on automated access to its site, so treat this as a personal/educational tool rather than something to run at scale or commercially — and don't scrape the raw HTML store page directly (this version avoids that entirely).

## License

Not yet licensed — add a `LICENSE` file (MIT is a common choice for portfolio projects) if you want others to be able to reuse the code.

## Known limitations

- Owner/revenue estimates are approximations, not verified sales data.
- Regional pricing, bundles, and sales history aren't factored in.
- Gemini output quality depends on how complete the store page's existing description already is.
