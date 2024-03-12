import recipe_crawler as rc
from user_class import User
import numpy as np
import pickle
import string
import utils
import time
import os

if __name__=='__main__':
    # Link to 30 minute recipes
    html_file = 'joc.html'
    url_file = 'joc_urls.p'
    pickle_recipes = 'pickle_recipes.p'
    web_address = 'https://www.justonecookbook.com'
    breaddress = 'https://www.justonecookbook.com/japanese-milk-bread-shokupan/'
    all_recipes = web_address + '/tags/under-30-minutes/'
    recipe_list = []   # List to hold all Recipe objects

    # Check website validity and permissions
    if not os.path.exists(html_file):
        # Get crawl permissions        
        rc.check_valid_website(web_address, robots=True)

        # Check if website urls valid
        rc.check_valid_website(all_recipes)

        # Check website crawl permissions
        # rc.check_crawl_permission(web_address, ['/', '/content'])

    names_list = []   # Will hold names of recipes with punctuation / capitals removed
    url_list = []   # Will hold urls of all recipes

    # Scrape urls for all recipes, or load urls if previously scraped
    if not os.path.exists(url_file):
        while True:
            # Get urls for all recipes
            print('Retrieving recipe urls')
            urls, all_recipes = rc.get_url_list(all_recipes, html_file, names_list, crawl_delay=0.25)
            url_list.extend(urls)

            if all_recipes is None:
                break

        # Save urls as pickle file for quick access
        with open(url_file, 'wb') as outfile:
            pickle.dump(url_list, outfile)

    else:
        # If we've already found the urls, load them in as list
        with open(url_file, 'rb') as infile:
            url_list = pickle.load(infile)
            url_list.append(breaddress)
    
    # Scrape all recipes, or load if already scraped
    if not os.path.exists(pickle_recipes):
        # Scrape each url
        print('Scraping recipes')
        i = 0
        for url in url_list:
            if i % 10 == 0:
                print(i)
            new_recipe = rc.scrape_recipes(url, html_file, names_list, crawl_delay=0.25)
            if new_recipe is not None:
                recipe_list.append(new_recipe)
            i += 1
            
        with open(pickle_recipes, 'wb') as outfile:
            pickle.dump(recipe_list, outfile)

    else:
        with open(pickle_recipes, 'rb') as infile:
            recipe_list = pickle.load(infile)
        print('Loaded recipes')
    

    # Get all unique ingredients
    unique_ingredients = utils.get_unique_ingredients(recipe_list)
    utils.set_ingredients_matrix(recipe_list, unique_ingredients)

    recipes_ingredients_matrix = utils.get_recipes_ingredients_matrix(recipe_list, len(unique_ingredients))
    with open('new_text.txt', 'w') as file:
        np.savetxt(file, recipes_ingredients_matrix)

    # print(recipes_ingredients_matrix)


    # USER STUFF
    user_id = 'Christian'
    christian = User(unique_ingredients, user_id) 

    user_id = 'Josh'
    josh = User(unique_ingredients, user_id)
    # print(christian.taste_profile_dict)
    print(josh.taste_profile_dict)
    print('*'*88)
    print(josh.taste_profile_weights)

    # os.remove(pickle_recipes)