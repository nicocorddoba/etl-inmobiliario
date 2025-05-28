from prefect import flow
from prefect.runner.storage import GitRepository
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
URL = os.getenv("URL")

repo = GitRepository(
    url = "https://github.com/nicocorddoba/etl-inmobiliario.git",
    name= "etl-inmobiliario",
    branch="task-develop")

# path = os.path.join(os.path.dirname(__file__), "raw")
PROVINCE_BY_DAY = {
    1: "tucuman",
    2: "cordoba",
    3: "mendoza",
    4: "santa-fe",
    5: "capital-federal"
}

def get_province_by_day() -> str:
    """
    Returns the province based on the day of the month.
    """
    today = datetime.today().day
    return PROVINCE_BY_DAY.get(today, "tucuman")  # Default to "tucuman" if day is not in the mapping


if __name__ == "__main__":
    flow.from_source(
        source=repo,
        entrypoint="main_etl.py:flujo_etl_inmobiliario"
        
    ).deploy(
        name="etl-inmobiliario",
        parameters={
            "url": URL,
            "province": get_province_by_day()
            # "path": path
        },
        work_pool_name="etl-workpool",
        cron = "0 0 1,10,20,28 * *"
        # tags=["etl", "inmobiliario"]
    )
