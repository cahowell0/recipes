import pickle
import recipe_crawler as rc

def get_unique_ingredients(recipe_list):
    """Gets list of unique ingredients, without duplicates
    
    Parameters:
        recipe_list (list): list containing Recipe objects
    """
    unique_ingredients = set()
    for recipe in recipe_list:
        unique_ingredients.update(list(recipe.ingredients.keys()))

    return unique_ingredients