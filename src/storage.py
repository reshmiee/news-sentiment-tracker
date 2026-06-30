import sqlite3
from datetime import datetime
from src.config import DB_PATH

def init_db():
    """Create the headlines table if it doesn't already exist."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS headlines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            headline TEXT,
            source TEXT,
            link TEXT,
            sentiment REAL,
            scraped_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_headlines(headlines):
    """Save a list of headline dicts (with sentiment scores) into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for h in headlines:
        cursor.execute("""
            INSERT INTO headlines (headline, source, link, sentiment, scraped_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            h["headline"],
            h["source"],
            h["link"],
            h["sentiment"],
            datetime.now().isoformat()
        ))

    conn.commit()
    conn.close()
    print(f"Saved {len(headlines)} headlines to database.")


# quick manual test
if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")