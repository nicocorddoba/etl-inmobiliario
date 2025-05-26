from playwright.sync_api import sync_playwright, Playwright, Page

def pagination(url, page: Page, browser ,logger,):
    try:
        page.goto(url)
        page.wait_for_selector("ul.pagination.pagination--links")
        number_of_pages = page.locator("li.pagination__page").nth(-2).inner_text()
        logger.info(f"Number of pages: {number_of_pages}")
    except:
        logger.error("Error: No se pudo cargar la pagina")
        browser.close()
        raise Exception("Error: No se pudo cargar la pagina")
    properties = []
    logger.info(f"Starting to scrape {number_of_pages} pages")
    for i in range(1, int(number_of_pages)):
        logger.info(f"Scraping page {i}")
        # scrap_rsarg scraps the data of each property
        data = scrap_rsarg(url + f"?pagina-{i}", page, browser, logger)
        properties.extend(data)
    return properties


def scrap_rsarg(url:str,page: Page,browser, logger):
    try:    
        if url[-1] != '1':
            page.goto(url)
            # logger.info(f"Scraping page {url[-1]}")

        page.wait_for_selector(".listing__items")   
        items = page.locator(".listing__item")
    except:
        logger.error("Error: No se pudo cargar la pagina")
        browser.close()
        raise Exception("Error: No se pudo cargar la pagina")
    items_count = items.count()
    properties = []
    logger.info("Starting to add items to list")
    for i in range(items_count):
        item = items.nth(i)
        adress = item.locator("p.card__address").inner_text()
        city = item.locator("p.card__title\\--primary").inner_text()
        price_currency = item.locator("p.card__price").inner_text()
        features = item.locator("ul.card__main-features").inner_text()
        title = item.locator("h2.card__title").inner_text()
        info = item.locator("p.card__info").inner_text()
        # text = item.inner_text()
        id = item.get_attribute("id")
        properties.append({
            "adress": adress,
            "city": city,
            "price_currency": price_currency,
            "features": features,
            "title": title,
            "info": info,
            "id": id
        })
        logger.info(f"Item {id} added")
    return properties

def run(url: str, logger = None, province: str = "tucuman") -> list[dict]:
    if logger is None:
        from utils.logger import get_logger
        logger = get_logger(__name__)
    with sync_playwright() as playwright:
        chromium = playwright.chromium # or "firefox" or "webkit".
        browser = chromium.launch(headless=True)
        context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 11.0; Win64; x64)...",
                viewport={"width": 1280, "height": 800},
                locale="en-US"
            )
        logger.info("Browser launched")
        page = context.new_page()
        # page.goto("http://example.com")
        url = url + province + "-arg"
        # Pagination gets the number of pages and scrapes each page
        data = pagination(url,page, browser, logger)
        browser.close()
    logger.info(f"Scraping completed, found {len(data)} of properties in {province}") 
    if len(data) < 1:
        logger.info(f"No data found")
        raise Exception("No data found")
    return data

