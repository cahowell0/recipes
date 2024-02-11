import time
import json
import string
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

# Save full html to file
def save_html(to_file, page_source):
    with open(to_file, 'w') as outfile:
        outfile.writelines(page_source)

# Find first recipe in list
def get_first_recipe_link(page_url, to_file, crawl_delay=0.5):
    current = None
    while not current:
        # Download page source
        page_source = requests.get(page_url).text
        save_html(to_file, page_source)   # Save html to file

        time.sleep(crawl_delay)   # Delay between crawls
        soup = bs(page_source, 'html.parser')
        current = soup.find(class_='m-PromoList__a-ListItem')   # Find first recipe
        # print(current.next_sibling.next_sibling.next_sibling.next_sibling.contents[0].get('href'))

        current = current.next_sibling.next_sibling.next_sibling.next_sibling

        # Extract link to first recipe
        first_recipe = current.contents[0].get('href')
        return 'https:' + first_recipe   # The link in the source begins with '//'

# Scrape recipes
def scrape_recipes(page_url, to_file, names_list, crawl_delay=0.5):
    current = None
    while not current:
        # Download page source
        page_source = requests.get(page_url).text
        save_html(to_file, page_source)   # Save html to file

        time.sleep(crawl_delay)   # Delay between crawls
        soup = bs(page_source, 'html.parser')
        current = soup.find(class_='o-AssetTitle__a-HeadlineText').text   # Find recipe name
        # print(current)

        # Check if recipe is duplicate
        if current.translate(str.maketrans('', '', string.punctuation)).lower() in names_list:
            # print(f'{current} already in list')
            return None
        
        else:
            # If new recipe, scrape and save
            with open(to_file, 'r') as infile:
                soup = bs(infile, 'html.parser')
                recipe = Recipe(page_url, soup)   # Create Recipe object

                return recipe

# Find next recipe
def get_next_recipe(page_url, to_file, crawl_delay=0.5):
    current = None
    while not current:
        # Download page source
        page_source = requests.get(page_url).text
        save_html(to_file, page_source)   # Save html to file

        time.sleep(crawl_delay)   # Delay between crawls
        soup = bs(page_source, 'html.parser')    
        
        current = soup.find(class_='o-AssetNavigation').contents[1].string   # Find script tag containing next url

        try:
            config_data = json.loads(current)

            if 'urls' in config_data:
                urls_list = config_data['urls']
                next_url = urls_list[0]
                return 'https:' + next_url

            else:
                print('No urls found')
        except json.JSONDecodeError as e:
            print(f'Error decoding JSON: {e}')
