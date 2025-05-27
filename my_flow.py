from prefect import flow
from prefect.runner.storage import GitRepository
import os
from dotenv import load_dotenv

load_dotenv()
URL = os.getenv("URL_INMOBILIARIO")

repo = GitRepository(
    url = "https://github.com/nicocorddoba/etl-inmobiliario.git",
    name= "etl-inmobiliario",
    branch="task-develop")

# path = os.path.join(os.path.dirname(__file__), "raw")

if __name__ == "__main__":
    flow.from_source(
        source=repo,
        entrypoint="main_etl.py:flujo_etl_inmobiliario"
        
    ).deploy(
        name="etl-inmobiliario",
        parameters={
            "url": URL,
            "province": "tucuman"
            # "path": path
        },
        work_pool_name="etl-workpool",
        cron = "0 0 1 * *",
        tags=["etl", "inmobiliario"]
    )
