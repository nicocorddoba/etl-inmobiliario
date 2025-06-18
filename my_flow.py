from prefect import flow
from prefect.runner.storage import GitRepository
import os


repo = GitRepository(
    url = "https://github.com/nicocorddoba/etl-inmobiliario.git",
    name= "etl-inmobiliario",
    branch="task-develop")

repo_api = GitRepository(
    url = "https://github.com/nicocorddoba/etl-farmacias.git",
    name = "sm-api",
    branch = "main"
)
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
    
    
    # Deploying the load flow for the API
    FB_URL = os.getenv("FB_URL")
    API_URL = os.getenv("API_URL")
    FB_EMAIL = os.getenv("FB_EMAIL")
    FB_PASSWORD = os.getenv("FB_PASSWORD")
    flow.from_source(
        source=repo_api,
        entrypoint="main_etl.py:flujo_carga_api"
    ).deploy(
        name="sm-api",
        parameters={
            "api_url": API_URL,
            "fb_url": FB_URL,
            "fb_email": FB_EMAIL,
            "fb_password": FB_PASSWORD
        },
        work_pool_name="ec2-work-pool",
        cron = "0 12 * * 2"
    )