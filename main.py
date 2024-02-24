import recipe_crawler as rc
import pickle
import string
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

    if not os.path.exists(html_file):
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

    if not os.path.exists(url_file):
        while True:
            # Get urls for all recipes
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
    
    for i, recipe in enumerate(recipe_list):
        if recipe is not None:
            # print(recipe, sep='\n')
            pass

    # os.remove(pickle_recipes)

