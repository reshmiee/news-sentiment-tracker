import sqlite3
import random
from datetime import datetime, timedelta
from src.scraper import fetch_headlines
from src.sentiment import get_sentiment
from src.storage import init_db, DB_PATH

def simulate_history(days=7):
    """Backfill fake historical data by re-using current headlines
    with randomized past timestamps and slightly jittered sentiment."""
    init_db()

    print("Fetching headlines to use as a base...")
    headlines = fetch_headlines()
    for h in headlines:
        h["sentiment"] = get_sentiment(h["headline"])

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    total_inserted = 0
    for day_offset in range(days, 0, -1):
        fake_date = datetime.now() - timedelta(days=day_offset)

        for h in headlines:
            # add small random jitter to sentiment so each day looks distinct
            jitter = random.uniform(-0.15, 0.15)
            jittered_sentiment = max(-1, min(1, h["sentiment"] + jitter))

            fake_timestamp = fake_date.replace(
                hour=random.randint(6, 22),
                minute=random.randint(0, 59)
            ).isoformat()

            cursor.execute("""
                INSERT INTO headlines (headline, source, link, sentiment, scraped_at)
                VALUES (?, ?, ?, ?, ?)
            """, (h["headline"], h["source"], h["link"], jittered_sentiment, fake_timestamp))
            total_inserted += 1

    conn.commit()
    conn.close()
    print(f"Inserted {total_inserted} simulated historical rows across {days} days.")


if __name__ == "__main__":
    simulate_history(days=7)