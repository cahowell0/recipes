import requests
from bs4 import BeautifulSoup as bs

import recipe_scraper
import recipe_crawler

if __name__=='__main__':
    # Link to all recipes in alphabetical order
    web_address = 'https://www.foodnetwork.com'
    all_recipes = web_address + '/recipes/recipes-a-z'

    # Get crawl permissions
    print(recipe_crawler.check_crawl_permission(web_address, ['/', '/content']))
    recipe_crawler.scrape_recipes(all_recipes)



    ##############################################
    ##############################################
    ##############################################



    # response = requests.get("https://www.foodnetwork.com/recipes/ree-drummond/nacho-cheese-casserole-5623818")   # Real website to scrape
    # # response = requests.get("https://www.foodnetwork.com/recipes/food-network-kitchen/nacho-cheese-sauce-13583364")   # Real website to scrape

    # # Save full html to file
    # with open(r'recipe.html', 'w') as outfile:
    #     outfile.writelines(response.text)

    # with open(r'recipe.html', 'r') as infile:
    #     soup = bs(infile, 'html.parser')
    #     print(recipe_scraper.get_recipe_name(soup))   # Print recipe name
    #     print(recipe_scraper.get_recipe_level(soup))   # Print recipe level
    #     print(recipe_scraper.get_recipe_times(soup))   # Print recipe times
    #     print(recipe_scraper.get_recipe_yield(soup))   # Print recipe yield
    #     print(recipe_scraper.get_ingredients(soup))   # Print recipe ingredients
    #     print(recipe_scraper.get_directions(soup))   # Print recipe directions

