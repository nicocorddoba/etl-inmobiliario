from prefect import task, get_run_logger
from prefect_aws.s3 import S3Bucket
import json
from datetime import datetime


@task
def load_data(province: str, data: list[dict]):
    logger = get_run_logger()
    try:
        logger.info("Starting saving data R2 bucket")
        s3 = S3Bucket.load("s3block-inmobiliaria")
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        today_str = datetime.now().strftime("%Y-%m-%d")
        object_name = f"{province}/{today_str}.json"
        s3.upload_from_string(
            data=json_str,
            key=object_name,
            # content_type="application/json"
        )
        # json.dump(data, open(path+ "\\" + today_str, "w", encoding="utf-8"), indent=2)
    except Exception as e:
        logger.error(f"Error during saving data: {e}")
        raise e