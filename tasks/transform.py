from prefect import task, get_run_logger

@task
def transform_data(data: list[dict]):
    logger = get_run_logger()
    transformed_data = []
    str
    for item in data:
        try:
            transformed_item = {
                "address": item.get("adress"),
                "city": item.get("city"),
                "price_currency": item.get("price_currency"),
                "features": item.get("features"),
                "title": item.get("title"),
                "info": item.get("info"),
                "id": item.get("id")
            }
            transformed_data.append(transformed_item)
        except Exception as e:
            logger.error(f"Error transforming item with ID: {item.get('id')}")
            raise e
    return transformed_data