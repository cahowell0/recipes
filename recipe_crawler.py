import time
import requests
import numpy as np
from urllib import robotparser
import recipe_scraper

# Check if allowed to access page + crawl delay
def check_crawl_permission(web_address, page_list=['/']):
    rp = robotparser.RobotFileParser()
    rp.set_url(web_address + '/robots.txt')
    rp.read()

    # Get required crawl delay
    crawl_delay = rp.crawl_delay('*')
    permissions = np.array([rp.can_fetch('*', web_address + page) for page in page_list])

    # Throw error if access denied
    if not all(permissions):
        raise ValueError(f'Permission denied for page {np.array(page_list)[np.invert(permissions)]}')
    return permissions, crawl_delay

def scrape_recipes(page):
    current = None
    while not current:
        # Download page source
        page_source = requests.get(page).text
        time.sleep(0.5)

        current = 1