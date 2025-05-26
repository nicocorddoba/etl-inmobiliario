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
                "currency": item.get("price_currency").split(" ")[0],
                "price": item.get("price_currency").split(" ")[1],
                "features": item.get("features"),
                "title": item.get("title"),
                "info": item.get("info"),
                "id": item.get("id")
            }
            transformed_data.append(transformed_item)
            logger.info(f"Transformed item with ID: {item.get('id')}")
        except Exception as e:
            logger.error(f"Error transforming item with ID: {item.get('id')}")
            raise e
    return transformed_data