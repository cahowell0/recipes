import recipe_crawler as rc
import string
import time
import os

if __name__=='__main__':
    # Link to all recipes in alphabetical order
    # to_file = 'foodnetwork.html'
    to_file = 'anyrecipe.html'
    # web_address = 'https://www.foodnetwork.com'
    web_address = 'https://anyrecipe.net/'
    # all_recipes = web_address + '/recipes/recipes-a-z'
    all_recipes = web_address + 'index1.html'
    recipe_list = []   # List to hold all Recipe objects

    """
    if not os.path.exists(to_file):
        # Get crawl permissions        
        rc.check_valid_website(web_address, robots=True)

        # Check if website urls valid
        rc.check_valid_website(all_recipes)

        # Check website crawl permissions
        rc.check_crawl_permission(web_address, ['/', '/content'])
        """

    # Get link to first recipe on foodnetwork.com
    # recipe_url = rc.get_first_recipe_link(all_recipes, to_file, crawl_delay=0.25)
    end = False
    count = 0
    names_list = []   # Will hold names of recipes with punctuation / capitals removed
    while not end:
        # Scrape recipe
        # print(recipe_url)
        new_recipe = rc.scrape_recipes(all_recipes, to_file, names_list, crawl_delay=0.25)
        # print('#########')

        """
        if new_recipe:   # Only add recipes that aren't already in names_list
            recipe_list.append(new_recipe)
            
            # Append recipe name with no capitals or punctuation
            names_list.append(new_recipe.recipe_name.translate(str.maketrans('', '', string.punctuation)).lower())

        # Crawl to next recipe
        # print('-----', recipe_url)
        recipe_url = rc.get_next_recipe(recipe_url, to_file, crawl_delay=0.25)

        count += 1
        # print(count)

        # if len(names_list) > 5 or count > 5:
            # end = 1   # Figure out when to stop
        """
        end = 1

    # print(recipe_list[0].directions)