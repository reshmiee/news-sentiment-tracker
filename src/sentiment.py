from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    """Return a compound sentiment score between -1 (negative) and +1 (positive)."""
    scores = analyzer.polarity_scores(text)
    return scores["compound"]


# quick manual test
if __name__ == "__main__":
    test_headlines = [
        "Markets soar to record high as economy booms",
        "Floods devastate region, hundreds displaced",
        "Central bank to meet Thursday to discuss rates",
    ]

    for headline in test_headlines:
        score = get_sentiment(headline)
        print(f"{score:+.2f}  {headline}")