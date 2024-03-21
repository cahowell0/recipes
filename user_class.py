from recipe_class import Recipe
import numpy as np
import pickle
import random

class User():
    def __init__(self, unique_ingredients, user_id, recipe_list):
        self.user_id = user_id
        self.taste_profile_dict = self.initialize_taste_profile(unique_ingredients)   # Ingredients that the user likes (weights)
        self.taste_profile_weights = [self.taste_profile_dict[unique_ingredients[i]] for i in range(len(unique_ingredients))]
        self.recommendation_table = None
        self.recipe_scores = None
        self.set_recipe_scores(recipe_list)

    
    def initialize_taste_profile(self, unique_ingredients):
        initial_weights = np.random.rand(len(unique_ingredients))

        return {unique_ingredients[i]: initial_weights[i] for i in range(len(unique_ingredients))}
    
    def save_taste_profile(self):
        with open(f'user_{self.user_id}.p', 'wb') as outfile:
            pickle.dump(self.user_id)
            pickle.dump(self.taste_profile_dict)
            pickle.dump(self.taste_profile_weights)
            pickle.dump(self.recommendation_table)

    def set_recipe_scores(self, recipe_list):
        self.recipe_scores = {recipe_list[i].recipe_name: 0 for i in range(len(recipe_list))}
