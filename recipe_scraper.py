import string

class Recipe():
    def __init__(self, url, soup):
        self.url = url
        self.recipe_name = self.scrape_recipe_name(soup)
        self.recipe_level = self.scrape_recipe_level(soup)         # Might want to turn this into an int in the future
        self.recipe_total_time, self.recipe_active_time = self.scrape_recipe_times(soup)    # Might want to turn these into ints in the future
        self.recipe_yield = self.scrape_recipe_yield(soup)         # Not sure if this one can be made an int
        self.ingredients = self.scrape_ingredients(soup)
        self.directions = self.scrape_directions(soup)
        self.num_ingredients = len(self.ingredients)
        self.num_directions = len(self.directions)

    # Scrape recipe name
    def scrape_recipe_name(self, soup):
        recipe_name = soup.find(class_="o-AssetTitle__a-HeadlineText")   # Get recipe name

        return str(recipe_name.string)

    # Scrape recipe level
    def scrape_recipe_level(self, soup):
        recipe_level = soup.find(class_='o-RecipeInfo__a-Headline', string='Level:')
        return str(recipe_level.next_sibling.next_sibling.string)

    # Scrape recipe time(s)
    def scrape_recipe_times(self, soup):
        # NEED TO CHANGE THIS TO ACCEPT 'PREP' AND 'COOK' AS OPTIONS AS WELL
        recipe_total_time = soup.find(class_='o-RecipeInfo__a-Description m-RecipeInfo__a-Description--Total')
        recipe_active_time = soup.find(class_='o-RecipeInfo__a-Headline', string='Active:')
        return str(recipe_total_time.string), str(recipe_active_time.next_sibling.next_sibling.string)

    # Scrape yield
    def scrape_recipe_yield(self, soup):
        recipe_yield = soup.find(class_='o-RecipeInfo__a-Headline', string='Yield:')
        return str(recipe_yield.next_sibling.next_sibling.string)

    # Scrape ingredients
    def scrape_ingredients(self, soup):
        ingredients = soup.find_all(class_='o-Ingredients__a-Ingredient--Checkbox')
        ingredients = [tag.get('value') for tag in soup.find_all(class_='o-Ingredients__a-Ingredient--Checkbox')]

        return ingredients[1:]   # The first 'ingredient' is 'deselect all'

    # Scrape directions
    def scrape_directions(self, soup):
        directions = [tag.string.strip() for tag in soup.find_all(class_='o-Method__m-Step')]
        return directions
