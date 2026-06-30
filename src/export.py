import sqlite3
import pandas as pd
from src.config import DB_PATH

EXPORT_PATH = "site/data.json"

def export_to_json():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM headlines", conn)
    conn.close()

    if df.empty:
        print("No data to export yet.")
        return

    # convert scraped_at to a proper datetime, then extract just the date
    df["scraped_at"] = pd.to_datetime(df["scraped_at"])
    df["date"] = df["scraped_at"].dt.date.astype(str)

    df.to_json(EXPORT_PATH, orient="records", date_format="iso")
    print(f"Exported {len(df)} rows to {EXPORT_PATH}")


if __name__ == "__main__":
    export_to_json()