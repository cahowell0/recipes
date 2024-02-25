from recipe_scraper import Recipe
import numpy

class User():
    def __init__(self):
        self.taste_profile = None   # Ingredients that the user likes (weights)
        self.recommendation_table = None   # 
