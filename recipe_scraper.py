import string
import re

class Recipe():
    def __init__(self, url, soup):
        self.url = url
        self.recipe_name = self.scrape_recipe_name(soup)
        # self.recipe_level = self.scrape_recipe_level(soup)         # Might want to turn this into an int in the future
        self.recipe_times_dict = self.scrape_recipe_times(soup)    # Might want to turn these into ints in the future
        self.recipe_servings = self.scrape_recipe_servings(soup)         # Not sure if this one can be made an int
        self.ingredients = self.scrape_ingredients(soup)
        # self.directions = self.scrape_directions(soup)
        # self.num_ingredients = len(self.ingredients)
        # self.num_directions = len(self.directions)

    # Scrape recipe name
    def scrape_recipe_name(self, soup):
        recipe_name = soup.find(class_="wprm-recipe-name wprm-block-text-bold").text   # Get recipe name

        # Throw error if no recipe name is found
        if recipe_name is None:
            raise ValueError(f'Recipe name not found')
        return str(recipe_name)

    # justonecookbook doesn't have a difficulty level
    # # Scrape recipe level
    # def scrape_recipe_level(self, soup):
    #     recipe_level = soup.find(class_='o-RecipeInfo__a-Headline', string='Level:')
    #     return str(recipe_level.next_sibling.next_sibling.string)

    # Scrape recipe time(s)
    def scrape_recipe_times(self, soup):
        recipe_times_html = soup.find(class_='details-servings').previous_sibling.previous_sibling
        recipe_times_dict = {}

        for t in recipe_times_html:
            time_text = t.contents[0].text[:-2]   # Remove semicolon and trailing whitespace
            time_string = t.contents[1].text   # Time given as string

            time_mins = self.convert_time(time_string)   # Convert time to minutes
            recipe_times_dict[time_text] = time_mins   # Create new value in dictionary

        return recipe_times_dict

    def convert_time(self, time_num):
        words = time_num.split(' ')
        mins = 0

        while len(words) > 0:
            next_word = words[0]

            # Check if next_word is number
            if next_word.isdigit():
                num  = int(next_word)

            # Convert hours to minutes
            elif next_word == 'hour' or next_word == 'hours':
                num *= 60
                mins += num
                num = 0

            # Add total number of minutes
            elif next_word == 'minutes':
                mins += num

            words.pop(0)   # Remove first word from list

        return mins

    # Scrape servings
    def scrape_recipe_servings(self, soup):
        # Create list of words in servings html text
        recipe_servings_string_list = soup.find(class_='details-servings').contents[1].text.split(' ')
        servings = None

        # Parse through words list searching for serving size
        while len(recipe_servings_string_list) > 0:
            next_word = recipe_servings_string_list[0]
            if next_word.isdigit():   # Check if next_word is quantity
                servings = int(next_word)
            recipe_servings_string_list.pop(0)   # Remove first element from list

        return servings

    # Scrape ingredients
    def scrape_ingredients(self, soup):
        ingredients_html = soup.find_all(class_='wprm-recipe-ingredient-name')
        ingredients_list = []
        for ingredient in ingredients_html:
            ingredients_list.append(ingredient.text)
        
        amounts_html = soup.find_all(class_='wprm-recipe-ingredient-amount')
        amounts_list = []
        for amount in amounts_html:
            amounts_list.append(amount.text)

        print(amounts_list)

    """
        print(ingredients)
        ingredients = [tag.get('value') for tag in soup.find_all(class_='o-Ingredients__a-Ingredient--Checkbox')]

        return ingredients[1:]   # The first 'ingredient' is 'deselect all'

    # Scrape directions
    def scrape_directions(self, soup):
        directions = [tag.string.strip() for tag in soup.find_all(class_='o-Method__m-Step')]
        return directions

        """