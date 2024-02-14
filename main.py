import recipe_crawler as rc
import string
import time
import os

if __name__=='__main__':
    # Link to all recipes in alphabetical order
    # to_file = 'foodnetwork.html'
    # web_address = 'https://www.foodnetwork.com'
    # all_recipes = web_address + '/recipes/recipes-a-z'

    # Link to 30 minute recipes
    to_file = 'joc.html'
    web_address = 'https://www.justonecookbook.com'
    all_recipes = web_address + '/tags/under-30-minutes/'
    recipe_list = []   # List to hold all Recipe objects

    if not os.path.exists(to_file):
        # Get crawl permissions        
        rc.check_valid_website(web_address, robots=True)

        # Check if website urls valid
        rc.check_valid_website(all_recipes)

        # Check website crawl permissions
        # rc.check_crawl_permission(web_address, ['/', '/content'])

    end = False
    count = 0
    names_list = []   # Will hold names of recipes with punctuation / capitals removed
    url_list = []   # Will hold urls of all recipes

    end = False
    # TODO: Save this list so we don't have to iterate through it every time
    while not end:
        # Get urls for all recipes
        urls, all_recipes = rc.get_url_list(all_recipes, to_file, names_list, crawl_delay=0.25)
        url_list.extend(urls)

        if all_recipes is None:
            end = 1

    print(len(url_list))

    # Scrape each url
    for url in url_list[:2]:
        new_recipe = rc.scrape_recipes(url, to_file, names_list, crawl_delay=0.25)
        
    
        """
        new_recipe = rc.scrape_recipes(all_recipes, to_file, names_list, crawl_delay=0.25)

        if new_recipe:   # Only add recipes that aren't already in names_list
            recipe_list.append(new_recipe)
            
            # Append recipe name with no capitals or punctuation
            names_list.append(new_recipe.recipe_name.translate(str.maketrans('', '', string.punctuation)).lower())

        # Crawl to next recipe
        recipe_url = rc.get_next_recipe(recipe_url, to_file, crawl_delay=0.25)
        """

    print(names_list)