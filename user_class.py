from recipe_class import Recipe
import numpy as np

class User():
    def __init__(self, unique_ingredients):
        self.taste_profile_dict = self.initialize_taste_profile(unique_ingredients)   # Ingredients that the user likes (weights)
        self.taste_profile_weights = [self.taste_profile_dict[unique_ingredients[i]] for i in range(len(unique_ingredients))]
        self.recommendation_table = None   # 

    def initialize_taste_profile(self, unique_ingredients):
        initial_weights = np.zeros(len(unique_ingredients))

        return {unique_ingredients[i]: initial_weights[i] for i in range(len(unique_ingredients))}