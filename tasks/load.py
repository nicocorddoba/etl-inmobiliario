from prefect import task, get_run_logger
import json

@task
def load_data(path: str, data: list[dict]):
    logger = get_run_logger()
    try:
        logger.info("Starting data loading")
        json.dump(data, open(path, "w", encoding="utf-8"), indent=2)
    except Exception as e:
        logger.error(f"Error during data loading: {e}")
        raise e