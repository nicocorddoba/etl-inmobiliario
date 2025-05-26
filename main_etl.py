from prefect import flow, get_run_logger

from tasks.extract import scrap_data
from tasks.transform import transform_data
from tasks.load import load_data

@flow
def flujo_etl_inmobiliario(url: str, province: str, path: str):
    logger = get_run_logger()
    
    logger.info("Starting data extraction")
    raw_data = scrap_data(url, province)
    logger.info("Extracted data successfully")
    
    logger.info("Starting data transformation")
    transformed_data = transform_data(raw_data)
    logger.info("Transformed data successfully")
    
    logger.info("Starting data loading")
    load_data(path, transformed_data)
    logger.info("Data loading completed successfully")
    logger.info("Closing the flow")