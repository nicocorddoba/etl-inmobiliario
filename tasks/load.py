from prefect import task, get_run_logger
from prefect_aws.s3 import S3Bucket
import json
from datetime import datetime

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
    today = datetime.today().day
    return PROVINCE_BY_DAY.get(today, "tucuman")

@task
def load_data(data: list[dict], province: str = get_province_by_day()):
    logger = get_run_logger()
    try:
        logger.info("Starting saving data R2 bucket")
        s3 = S3Bucket.load("s3block-inmobiliaria")
        json_bytes = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
        today_str = datetime.now().strftime("%Y-%m-%d")
        object_name = f"{province}/{today_str}.json"
        s3.write_path(
            path=object_name,   # ⬅ nombre del objeto en el bucket
            content=json_bytes        # ⬅ contenido en bytes
        )
        # json.dump(data, open(path+ "\\" + today_str, "w", encoding="utf-8"), indent=2)
    except Exception as e:
        logger.error(f"Error during saving data: {e}")
        raise e