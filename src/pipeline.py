from src.scraper import fetch_headlines
from src.sentiment import get_sentiment
from src.storage import init_db, save_headlines

def run_pipeline():
    init_db()

    print("Fetching headlines...")
    headlines = fetch_headlines()

    print("Scoring sentiment...")
    for h in headlines:
        h["sentiment"] = get_sentiment(h["headline"])

    save_headlines(headlines)

    print(f"\nDone. {len(headlines)} headlines fetched, scored, and saved.")


if __name__ == "__main__":
    run_pipeline()