from playwright.sync_api import sync_playwright, Page
from bs4 import BeautifulSoup

def pagination(url, page: Page, logger):
    try:
        page.goto(url)
        page.route("**/*", lambda route, request: route.abort() if request.resource_type in ["image", "font", "media"] else route.continue_())
        
        page.wait_for_selector("ul.pagination.pagination--links")
        number_of_pages = page.locator("li.pagination__page").nth(-2).inner_text()
    except Exception as e:
        logger.error("Error: No se pudo cargar la pagina")
        raise
    
    properties = []
    logger.info(f"Starting to scrape {number_of_pages} pages")
    for i in range(1, int(number_of_pages) + 1):
        data = scrap_propertie_details(url + f"?pagina-{i}", page, logger)
        properties.extend(data)
        
        # Scraping 40 pages as limit to avoid overloading the server
        if i >= 40:
            logger.info("40 paginaciónes alcanzadas, deteniendo la paginación")
            break
    return properties


def scrap_propertie_details(url:str,page: Page, logger):
    try:
        if page.is_closed():
            logger.warning("Página cerrada, reabriendo nueva página")
            page = page.context.new_page()
        try:
            for attempt in range(2):
                page.goto(url, timeout=60000)
                break
        except TimeoutError as e:
            logger.warning(f"Timeout al intentar acceder a {url}, intento {attempt + 1}/2")
            if attempt == 2:
                raise
            import time
            time.sleep(5)
            
        page.wait_for_selector(".listing__items", timeout=40000)
        items = page.locator(".listing__item")
    except Exception as e:
        logger.error(f"Error: No se pudo cargar la página {url} (linea 36): {e}")
        raise
    
    items_count = items.count()
    properties = []

    for i in range(items_count):
        item = items.nth(i)
        
        
        item_html = item.inner_html()
        soup = BeautifulSoup(item_html, "html.parser")
        
        def get_text(sel):
            tag = soup.select_one(sel)
            return tag.get_text(strip=True) if tag else None
        id = soup.select_one("[data-item-card]")["data-item-card"] if soup.select_one("[id]") else None
        adress= get_text("p.card__address") 
        city = get_text("p.card__title--primary")
        price_currency = get_text("p.card__price")
        features = get_text("ul.card__main-features")
        title = get_text("h2.card__title")
        info = get_text("p.card__info") 
        properties.append({
            "adress": adress,
            "city": city,
            "price_currency": price_currency,
            "features": features,
            "title": title,
            "info": info,
            "id": id
        })
    return properties


def run(url: str, logger = None, province: str = "tucuman") -> list[dict]:
    if logger is None:
        from utils.logger import get_logger
        logger = get_logger(__name__)
    with sync_playwright() as playwright:
        logger.info("Province: " + province)
        chromium = playwright.chromium # or "firefox" or "webkit".
        browser = chromium.launch(headless=True, args=[
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--disable-software-rasterizer",
            "--no-sandbox",
            "--disable-extensions",
            "--disable-background-networking",
            "--disable-sync",
            "--disable-default-apps",
            "--mute-audio",
            # "--single-process" # Muy importante en instancias con poca RAM # DISCLAIMER: Parece cerrar el navegador
            "--no-zygote"
            
        ])
        context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 11.0; Win64; x64)...",
                viewport={"width": 1280, "height": 800},
                locale="en-US"
            )
        # context.set_default_timeout(10000)
        # context.set_default_navigation_timeout(10000)
        logger.info("Browser launched")
        page = context.new_page()

        url = url + province + "-arg"
        # Pagination gets the number of pages and scrapes each page
        data = pagination(url, page, logger)
        browser.close()
    if len(data) < 1:
        logger.info(f"No data found")
        raise Exception("No data found")
    
    logger.info(f"Scraping completed, found {len(data)} of properties in {province}") 
    return data

