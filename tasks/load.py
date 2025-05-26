from prefect import task, get_run_logger
import json
from datetime import datetime


@task
def load_data(path: str, data: list[dict]):
    logger = get_run_logger()
    try:
        logger.info("Starting data loading")
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        json.dump(data, open(path+ "\\" + today_str, "w", encoding="utf-8"), indent=2)
    except Exception as e:
        logger.error(f"Error during data loading: {e}")
        raise e