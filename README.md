# News Sentiment Tracker

A Python project that scrapes live news headlines via RSS, scores their sentiment using VADER, stores the data in SQLite, and visualizes sentiment trends over time on a custom-built static dashboard.

## What it does

- Pulls live headlines from BBC, Al Jazeera, and NYT via their public RSS feeds
- Scores each headline's sentiment (-1 to +1) using VADER (rule-based sentiment analysis)
- Stores every scrape in a local SQLite database, building historical data over time
- Visualizes average sentiment per source as a trend line over time
- Displays a table of recent headlines, color-coded by sentiment
- Includes two charting implementations for comparison: Chart.js (custom HTML/CSS/JS) and Plotly (Python-generated)

## Tech stack

- **Python** — feedparser, vaderSentiment, pandas, plotly
- **SQLite** — local data storage, no server required
- **HTML/CSS/JS** — hand-built static dashboard (no framework)
- **Chart.js** — interactive line chart, fully custom-styled
- **Plotly** — auto-generated interactive chart, used as a comparison

## Project structure

```
news-sentiment-tracker/
├── src/
│   ├── config.py            # RSS feed URLs, DB path
│   ├── scraper.py           # fetches headlines via feedparser
│   ├── sentiment.py         # scores headlines with VADER
│   ├── storage.py           # saves/reads from SQLite
│   ├── pipeline.py          # runs scraper → sentiment → storage in one go
│   ├── scheduler.py         # runs the pipeline on a loop (hourly)
│   ├── export.py            # exports DB → site/data.json
│   ├── plot_with_plotly.py  # generates standalone Plotly chart
│   └── simulate.py          # backfills historical data for testing
├── data/
│   └── headlines.db         # SQLite database (auto-created, gitignored)
├── site/
│   ├── index.html           # dashboard (chart + headline table)
│   ├── style.css
│   ├── script.js             # Chart.js logic
│   ├── data.json            # exported data (gitignored)
│   └── plotly_chart.html    # Plotly comparison chart
├── requirements.txt
└── README.md
```

## How to run it

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the full pipeline once (scrape → score → save):
```bash
python -m src.pipeline
```

3. Export the data for the dashboard:
```bash
python -m src.export
```

4. Serve the dashboard locally:
```bash
cd site
python -m http.server 8000
```
Then open `http://localhost:8000` in your browser.

5. (Optional) Generate the Plotly comparison chart:
```bash
python -m src.plot_with_plotly
```
Open `site/plotly_chart.html` directly in your browser.

6. (Optional) Run continuously to build real historical data:
```bash
python -m src.scheduler
```
This re-runs the pipeline every hour, accumulating real sentiment data over days/weeks.

## Notes & limitations

- VADER is a lightweight, rule-based sentiment tool — it performs well on emotionally clear headlines but can miss domain-specific language (e.g. financial terms like "soar" or "plunge" may register as neutral).
- Sentiment reflects the *tone of the headline's wording*, not necessarily the real-world significance of the event.
- Data only accumulates from the point you start running the scraper — no historical backfill from before that (the `simulate.py` script exists purely to generate fake test data for development).

## Possible future improvements

- Add more RSS sources
- Swap VADER for a transformer-based model (e.g. DistilBERT) for more nuanced scoring
- Add filtering by source/date range on the dashboard
- Deploy the static dashboard (e.g. GitHub Pages) so it's viewable without running a local server