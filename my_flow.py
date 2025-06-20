from prefect import flow
from prefect.runner.storage import GitRepository
import os


repo = GitRepository(
    url = "https://github.com/nicocorddoba/etl-inmobiliario.git",
    name= "etl-inmobiliario",
    branch="task-develop")

# path = os.path.join(os.path.dirname(__file__), "raw")

if __name__ == "__main__":
    # load_dotenv()
    URL = os.getenv("URL")
    flow.from_source(
        source=repo,
        entrypoint="main_etl.py:flujo_etl_inmobiliario"
        
    ).deploy(
        name="etl-inmobiliario",
        parameters={
            "url": URL
            # "path": path
        },
        work_pool_name="ec2-work-pool",
        cron = "0 0 1,10,20,28 * *"
        # tags=["etl", "inmobiliario"]
    )
