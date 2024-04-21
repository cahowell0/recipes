import re
import unicodedata
import numpy as np

class Recipe():
    def __init__(self, url, soup):
        self.url = url
        self.recipe_name = self.scrape_recipe_name(soup)
        # self.recipe_level = self.scrape_recipe_level(soup)         # Might want to turn this into an int in the future
        self.recipe_times_dict = self.scrape_recipe_times(soup)    # Might want to turn these into ints in the future
        self.recipe_servings = self.scrape_recipe_servings(soup)         # Not sure if this one can be made an int
        self.ingredients = self.scrape_ingredients(soup)
        self.instructions = self.scrape_instructions(soup)
        self.num_ingredients = len(self.ingredients)
        self.num_instructions = len(self.instructions)

        self.ingredients_matrix = []

    # Scrape recipe name
    def scrape_recipe_name(self, soup):
        """Scrape recipe name from the provided BeautifulSoup soup object

        Parameters:
            soup (BeautifulSoup): The BeautifulSoup object containing the recipe information

        Returns:
            recipe_name (str): The name of the recipe
        """
        recipe_name = soup.find(class_="wprm-recipe-name wprm-block-text-bold").text   # Get recipe name

        # Throw error if no recipe name is found
        if recipe_name is None:
            raise ValueError(f'Recipe name not found')
        return str(recipe_name)


    """
    # justonecookbook doesn't have a difficulty level
    # Scrape recipe level
    def scrape_recipe_level(self, soup):
        recipe_level = soup.find(class_='o-RecipeInfo__a-Headline', string='Level:')
        return str(recipe_level.next_sibling.next_sibling.string)
    """

    # Scrape recipe time(s)
    def scrape_recipe_times(self, soup):
        """
        Scrape the recipe times from the provided BeautifulSoup soup object

        Parameters:
            soup (BeautifulSoup): The BeautifulSoup object containing the recipe information

        Returns:
            recipe_time_dict (dict): Dictionary containing the scraped recipe times
        """
        recipe_times_html = soup.find(class_='details-servings').previous_sibling.previous_sibling
        recipe_times_dict = {}

        if recipe_times_html is None:
            raise ValueError(f'No times found for recipe {self.recipe_name}')

        for time_tag in recipe_times_html:
            time_text = time_tag.contents[0].text[:-2]   # Remove semicolon and trailing whitespace
            time_string = time_tag.contents[1].text   # Time given as string

            time_mins = self.convert_time(time_string)   # Convert time to minutes
            recipe_times_dict[time_text] = time_mins   # Create new value in dictionary

        return recipe_times_dict
        

    def convert_time(self, time_num):
        """Convert provided time to minutes"""
        words = time_num.split(' ')
        mins = 0
        num = 0

        for next_word in words:
            # Check if next_word is number
            if next_word.isdigit():
                num = int(next_word)

            # Convert hours to minutes
            elif next_word in {'hour', 'hours', 'hr', 'hrs'}:
                mins += num*60
                num = 0

            # Add total number of minutes
            elif next_word in {'mins', 'minutes'}:
                mins += num

        return mins

    # Scrape servings
    def scrape_recipe_servings(self, soup):
        # Create list of words in servings html text
        recipe_servings_string_list = soup.find(class_='details-servings').contents[1].text.split(' ')
        servings = None

        if recipe_servings_string_list is None:
            raise ValueError(f'No servings found for recipe {self.recipe_name}')

        # Parse through words list searching for serving size
        for next_word in recipe_servings_string_list:
            next_word = recipe_servings_string_list[0]
            if next_word.isdigit():   # Check if next_word is quantity
                servings = int(next_word)

        return servings

    # Scrape ingredients
    def scrape_ingredients(self, soup):
        # Scrape each ingredient text
        ingredients_html = soup.find_all(class_='wprm-recipe-ingredient-name')

        if ingredients_html is None:
            raise ValueError(f'No ingredients found for recipe {self.recipe_name}')

        # Create list of ingredients
        pattern = re.compile(r'.+?(?= \()')   # This will match the ingredients up until the opening parenthesis
        ingredients_list = [re.match(pattern, ingredient.text).group() if re.match(pattern, ingredient.text) else ingredient.text for ingredient in ingredients_html]   # This ugly code adds the ingredients without the paraentheses

        # Scrape amount for each ingredient
        amounts_html = soup.find_all(class_='wprm-recipe-ingredient-amount')
        amounts_list = [amount.text for amount in amounts_html]
        amounts_list = [self.vulgar_fraction_to_float(amount.text) for amount in amounts_html]

        # TODO: Ingredients and amounts aren't always same length

        return dict(zip(ingredients_list, amounts_list))

    def vulgar_fraction_to_float(self, vulgar_fraction):
        """Convert vulgar (single-character) fractions to floats"""
        decimal = '0'
        fraction = 0
        for num in vulgar_fraction:
            try:
                if unicodedata.digit(num):
                    decimal += num
            except:
                try:
                    if unicodedata.numeric(num):
                        fraction += unicodedata.numeric(num)
                except:
                    if not num.alnum():
                        break
                    else:
                        raise ValueError(f'{self.recipe_name} is having an amounts error')
                    
        decimal = int(decimal)
        
        return decimal + fraction

    # Scrape instructions
    def scrape_instructions(self, soup):
        instructions_html = soup.find_all(class_='wprm-recipe-instruction-text')

        if instructions_html is None:
            raise ValueError(f'No instructions found for recipe {self.recipe_name}')

        instructions = [instruction.text for instruction in instructions_html]

        return instructions   # Skip the first
        
    def set_ingredients(self, unique_ingredients):
        self.ingredients_matrix = np.zeros(len(unique_ingredients))

        for i, ingredient in enumerate(unique_ingredients):
            if ingredient in self.ingredients:
                self.ingredients_matrix[i] = 1

    def __str__(self):
        name_str = f'RECIPE NAME: {self.recipe_name}'
        num_ingredients_str = f'NUM INGREDIENTS: {self.num_ingredients}'
        num_instructions_str = f'NUM INSTRUCTIONS: {self.num_instructions}'

        return f'{name_str}\n{num_ingredients_str}\n{num_instructions_str}'