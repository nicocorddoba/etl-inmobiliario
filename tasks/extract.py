from prefect import task, get_run_logger
from plugins.scrap import run as scrap_run
from datetime import datetime
import pytz

PROVINCE_BY_DAY = {
    1: "tucuman",
    10: "cordoba",
    20: "mendoza",
    28: "santa-fe",
}

def get_province_by_day() -> str:
    """
    Returns the province based on the day of the month.
    """
    today = datetime.now(pytz.timezone("America/Argentina/Buenos_Aires")).day
    print(f"Today is day {today} of the month.")
    return PROVINCE_BY_DAY.get(today, "tucuman")

@task
def scrap_data(url: str, province: str = get_province_by_day()):
    try:
        logger = get_run_logger()
        data = scrap_run(url, logger, province)
    except Exception as e:
        logger.error(f"Error during data extraction: {e}")
        raise e
    return data, province