import pickle
import numpy as np
import recipe_crawler as rc

def get_unique_ingredients(recipe_list):
    """Gets list of unique ingredients, without duplicates
    
    Parameters:
        recipe_list (list): list containing Recipe objects
    """
    unique_ingredients = set()
    for recipe in recipe_list:
        unique_ingredients.update(list(recipe.ingredients.keys()))

    return sorted(list(unique_ingredients))

def set_ingredients_matrix(recipe_list, unique_ingredients):
    """Creates ingredients matrix attribute for each recipe
    
    Parameters:
        recipe_list (list): list containing Recipe objects
        unique_ingredients (list): list containing all ingredients in all recipes
    """
    for recipe in recipe_list:
        recipe.set_ingredients(unique_ingredients)

def get_recipes_ingredients_matrix(recipe_list, num_unique_ingredients):
    """Creates matrix of all recipes with the ingredients that they contain
    
    Parameters:
        recipe_list (list): list containing Recipe objectes
        num_unique_ingredients (int): number of total unique ingredients across all recipes
    """
    recipes_ingredients_matrix = np.zeros(num_unique_ingredients)   # This is just to initialize the matrix, but will be deleted later
    for recipe in recipe_list:
        # Create matrix where each row contains the ingredients for a new recipe
        recipes_ingredients_matrix = np.vstack((recipes_ingredients_matrix, recipe.ingredients_matrix))
    
    # Delete the first row of zeros
    recipes_ingredients_matrix = np.delete(recipes_ingredients_matrix, (0), axis=0)

    return recipes_ingredients_matrix

def get_users_ingredients_matrix(user_list, num_unique_ingredients):
    """Creates matrix of all users and their ingredient profiles
    
    Parameters:
        user_list (list): list containing User objects
        num_unique_ingredients (int): number of total unique ingredients across all recipes
    """
    user_ingredients_matrix = np.zeros(num_unique_ingredients)   # Placeholder that will be deleted later
    for user in user_list:
        # Create matrix where each row containg the users preference for individual recipes
        user_ingredients_matrix = np.vstack((user_ingredients_matrix, user.taste_profile_weights))

    # Delete the first row of zeros
    user_ingredients_matrix = np.delete(user_ingredients_matrix, (0), axis=0)

    return user_ingredients_matrix

def cos_similarity(user1, user_list):
    """Uses cosine similarity to find the users with the closest taste profile
    
    Parameters:
        user1 (User): the user whose profile we are updating
        user_list (list): list of User objects to compare with user1
    """
    closest_user = np.inf

    # Maybe there is a more efficient way of doing this, without calculating it for each user?
    for user in user_list:
        sim = np.dot(user1, user) / (np.norm(user1) * np.norm(user))

        # Find the most similar user
        if sim < closest_user:
            closest_user = user

    return closest_user