from prefect import flow, get_run_logger

from tasks.extract import scrap_data
from tasks.transform import transform_data
from tasks.load import load_data

@flow
def flujo_etl_inmobiliario(url: str):
    logger = get_run_logger()
    
    logger.info("Starting data extraction")
    raw_data, province = scrap_data(url = url)
    logger.info("Extracted data successfully")
    
    logger.info("Starting data transformation")
    transformed_data = transform_data(raw_data)
    logger.info("Transformed data successfully")
    
    logger.info("Starting data loading")
    load_data(data = transformed_data, province = province)
    logger.info("Data loading completed successfully")
    logger.info("Closing the flow")