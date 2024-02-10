import requests
from bs4 import BeautifulSoup as bs
import os
import re

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
    ingredients = soup.find_all(class_='o-Ingredients__a-Ingredient--Checkbox')
    ingredients = [tag.get('value') for tag in soup.find_all(class_='o-Ingredients__a-Ingredient--Checkbox')]
    
    return ingredients[1:]   # The first 'ingredient' is 'deselect all'

# Get directions
def get_directions(soup):
    directions = [tag.string.strip() for tag in soup.find_all(class_='o-Method__m-Step')]
    return directions
