import time
import requests
import numpy as np
from urllib import robotparser
from bs4 import BeautifulSoup as bs
from recipe_scraper import Recipe

# Check for valid website
def check_valid_website(web_address, robots=False):
    if robots:   # Check if robots.txt exists
        try:
            robots_response = requests.head(web_address)
            robots_response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f'Error checking validity: {e}')

    else:   # Check if base page exists
        try:
            response = requests.head(web_address)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f'Error checking validity: {e}')
            return False

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
    return crawl_delay

# Find first recipe in list
def get_first_recipe(page, crawl_delay=5):
    current = None
    while not current:
        # Download page source
        page_source = requests.get(page).text
        time.sleep(crawl_delay)   # Delay between crawls

        soup = bs(page_source, 'html.parser')
        current = soup.find(class_='m-PromoList__a-ListItem')   # Find first recipe

        # Extract link to first recipe
        first_recipe = current.contents[0].get('href')
        return first_recipe[2:]   # The link in the source begins with '//'


