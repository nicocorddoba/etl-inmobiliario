from prefect import task, get_run_logger

@task
def scrap_data(url: str):
    try:
        data = {}
    except Exception as e:
        logger = get_run_logger()
        logger.error(f"Error during data extraction: {e}")
        raise e
    return data