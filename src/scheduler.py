import time
from src.pipeline import run_pipeline

# how often to run the pipeline, in seconds
INTERVAL_SECONDS = 60 * 60  # 1 hour

def start_scheduler():
    while True:
        print("\n--- Running pipeline ---")
        run_pipeline()
        print(f"Sleeping for {INTERVAL_SECONDS // 60} minutes...\n")
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    start_scheduler()