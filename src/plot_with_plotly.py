import sqlite3
import pandas as pd
import plotly.express as px
from src.config import DB_PATH

OUTPUT_PATH = "site/plotly_chart.html"

def generate_plotly_chart():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM headlines", conn)
    conn.close()

    if df.empty:
        print("No data to plot yet.")
        return

    df["scraped_at"] = pd.to_datetime(df["scraped_at"])
    df["date"] = df["scraped_at"].dt.date.astype(str)

    # average sentiment per day, per source
    daily_avg = df.groupby(["date", "source"])["sentiment"].mean().reset_index()

    fig = px.line(
        daily_avg,
        x="date",
        y="sentiment",
        color="source",
        markers=True,
        title="News Sentiment Over Time (Plotly)",
        labels={"sentiment": "Avg Sentiment", "date": "Date", "source": "Source"}
    )

    fig.update_yaxes(range=[-1, 1])
    fig.write_html(OUTPUT_PATH, include_plotlyjs="cdn")
    print(f"Plotly chart saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    generate_plotly_chart()