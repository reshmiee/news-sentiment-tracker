import feedparser
from src.config import RSS_FEEDS

def fetch_headlines():
    """Fetch latest headlines from all configured RSS feeds."""
    all_headlines = []

    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            all_headlines.append({
                "headline": entry.title,
                "source": source,
                "link": entry.link,
                "published": entry.get("published", "")
            })

    return all_headlines


# quick manual test
if __name__ == "__main__":
    headlines = fetch_headlines()
    print(f"Fetched {len(headlines)} headlines\n")
    for h in headlines[:88]:
        print(f"[{h['source']}] {h['headline']}")