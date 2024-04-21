from recipe_class import Recipe
import numpy as np
import pickle
import random

class User():
    def __init__(self, unique_ingredients, user_id, recipe_list):
        self.user_id = user_id
        self.ingredient_scores_dict = self.initialize_taste_profile(unique_ingredients)   # Ingredients that the user likes (weights)
        self.ingredient_weights = [self.ingredient_scores_dict[unique_ingredients[i]] for i in range(len(unique_ingredients))]
        self.recommendation_table = None
        self.recipe_scores = None
        self.set_recipe_scores(recipe_list)

    def initialize_taste_profile(self, unique_ingredients):
        initial_weights = np.round(np.random.rand(len(unique_ingredients)), 4)

        return {unique_ingredients[i]: initial_weights[i] for i in range(len(unique_ingredients))}
    
    def save_taste_profile(self):
        with open(f'user_{self.user_id}.p', 'wb') as outfile:
            pickle.dump(self.user_id)
            pickle.dump(self.ingredient_scores_dict)
            pickle.dump(self.ingredient_weights)
            pickle.dump(self.recommendation_table)

    def set_recipe_scores(self, recipe_list):
        self.recipe_scores = {recipe_list[i].recipe_name: 0 for i in range(len(recipe_list))}

    def ingredient_to_recipe_score_conversion(self, recipe_list):
        for recipe in recipe_list:
            recipe_score = np.sum(recipe.ingredients_matrix * self.ingredient_weights) / np.sum(recipe.ingredients_matrix)
            if recipe_score <= 0.15:
                recipe_rating = 1
            elif recipe_score <= 0.3:
                recipe_rating = 2
            elif recipe_score <= 0.5:
                recipe_rating = 3
            elif recipe_score <= 0.75:
                recipe_rating = 4
            else:
                recipe_rating = 5

            self.recipe_scores[recipe.recipe_name] = recipe_rating
        

    def __str__(self):
        return f'{str(self.user_id).upper()}'