import requests
from bs4 import BeautifulSoup as bs
import re

response = requests.get("https://www.foodnetwork.com/recipes/ree-drummond/nacho-cheese-casserole-5623818")   # Real website to scrape
# response = requests.get("https://www.foodnetwork.com/recipes/food-network-kitchen/nacho-cheese-sauce-13583364")   # Real website to scrape

# print(response.status_code, response.ok, response.reason)   # Check website status
# print(response.text)   # Print full html

# Get recipe name
def get_recipe_name(soup):
    recipe_name = soup.find(class_="o-AssetTitle__a-HeadlineText")   # Get recipe name
    return recipe_name.string

# Get recipe level
def get_recipe_level(soup):
    recipe_level = soup.find(class_='o-RecipeInfo__a-Headline', string='Level:')
    return recipe_level.next_sibling.next_sibling.string

# Get recipe time(s)
def get_recipe_times(soup):
    recipe_total_time = soup.find(class_='o-RecipeInfo__a-Description m-RecipeInfo__a-Description--Total')
    recipe_active_time = soup.find(class_='o-RecipeInfo__a-Headline', string='Active:')
    return recipe_total_time.string, recipe_active_time.next_sibling.next_sibling.string

# Get yield
def get_recipe_yield(soup):
    recipe_yield = soup.find(class_='o-RecipeInfo__a-Headline', string='Yield:')
    return recipe_yield.next_sibling.next_sibling.string

# Get ingredients
def get_ingredients(soup):
    # ingredients = [tag.string.strip() for tag in soup.find_all(class_='o-Ingredients__a-Ingredient--Checkbox')]
    ingredients = soup.find_all(class_='o-Ingredients__a-Ingredient--Checkbox')
    ingredients = [tag.get('value') for tag in soup.find_all(class_='o-Ingredients__a-Ingredient--Checkbox')]
    
    return ingredients[1:]

# Get directions
def get_directions(soup):
    directions = [tag.string.strip() for tag in soup.find_all(class_='o-Method__m-Step')]
    return directions


if __name__=='__main__':
    # Save full html to file
    with open(r'recipe.html', 'w') as outfile:
        outfile.writelines(response.text)

    with open(r'recipe.html', 'r') as infile:
        soup = bs(infile, 'html.parser')
        print(get_recipe_name(soup))   # Print recipe name
        print(get_recipe_level(soup))   # Print recipe level
        print(get_recipe_times(soup))   # Print recipe times
        print(get_recipe_yield(soup))   # Print recipe yield
        print(get_ingredients(soup))   # Print recipe ingredients
        print(get_directions(soup))   # Print recipe directions
