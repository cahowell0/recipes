import recipe_crawler
import time

if __name__=='__main__':
    # Link to all recipes in alphabetical order
    web_address = 'https://www.foodnetwork.com'
    all_recipes = web_address + '/recipes/recipes-a-z'

    # Get crawl permissions
    # time1 = time.perf_counter()

    recipe_crawler.check_valid_website(web_address, robots=True)
    # time2 = time.perf_counter()
    # print('check valid website:', time2 - time1)

    recipe_crawler.check_valid_website(all_recipes)
    # time3 = time.perf_counter()
    # print('check valid website (all recipes):', time3 - time2)

    recipe_crawler.check_crawl_permission(web_address, ['/', '/content'])
    # time4 = time.perf_counter()
    # print('check crawl permission:', time4 - time3)

    first_recipe = recipe_crawler.get_first_recipe(all_recipes)
    # time5 = time.perf_counter()
    # print('get first recipe:', time5 - time4)

    # recipe_crawler.scrape_recipes()





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
        # print(recipe_scraper.scrape_recipe_name(soup))   # Print recipe name
        # print(recipe_scraper.scrape_recipe_level(soup))   # Print recipe level
    #     print(recipe_scraper.scrape_recipe_times(soup))   # Print recipe times
    #     print(recipe_scraper.scrape_recipe_yield(soup))   # Print recipe yield
    #     print(recipe_scraper.scrape_ingredients(soup))   # Print recipe ingredients
    #     print(recipe_scraper.scrape_directions(soup))   # Print recipe directions

