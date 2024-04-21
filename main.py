import recipe_crawler as rc
from user_class import User
import numpy as np
import pickle
import string
import utils
import time
import os
from sklearn.metrics.pairwise import cosine_similarity as cosine_similarity
from sklearn.neighbors import NearestNeighbors as NearestNeighbors

if __name__=='__main__':
    # Link to 30 minute recipes
    # https://www.justonecookbook.com/tags/under-30-minutes
    html_file = 'joc.html'
    url_file = 'joc_urls.p'
    pickle_recipes = 'pickle_recipes.p'
    web_address = 'https://www.justonecookbook.com'
    breaddress = 'https://www.justonecookbook.com/japanese-milk-bread-shokupan/'
    all_recipes = web_address + '/tags/under-30-minutes/'
    recipe_list = []   # List to hold all Recipe objects

    # Check website validity and permissions
    if not os.path.exists(html_file):
        # Get crawl permissions        
        rc.check_valid_website(web_address, robots=True)

        # Check if website urls valid
        rc.check_valid_website(all_recipes)

        # Check website crawl permissions
        # rc.check_crawl_permission(web_address, ['/', '/content'])

    names_list = []   # Will hold names of recipes with punctuation / capitals removed
    url_list = []   # Will hold urls of all recipes

    # Scrape urls for all recipes, or load urls if previously scraped
    if not os.path.exists(url_file):
        while True:
            # Get urls for all recipes
            print('Retrieving recipe urls')
            urls, all_recipes = rc.get_url_list(all_recipes, html_file, names_list, crawl_delay=0.25)
            url_list.extend(urls)

            if all_recipes is None:
                break

        # Save urls as pickle file for quick access
        with open(url_file, 'wb') as outfile:
            pickle.dump(url_list, outfile)

    else:
        # If we've already found the urls, load them in as list
        with open(url_file, 'rb') as infile:
            url_list = pickle.load(infile)
            url_list.append(breaddress)

    # Scrape all recipes, or load if already scraped
    if not os.path.exists(pickle_recipes):
        # Scrape each url
        print('Scraping recipes')
        i = 0
        for url in url_list:
            if i % 10 == 0:
                print(i)
            new_recipe = rc.scrape_recipes(url, html_file, names_list, crawl_delay=0.25)
            if new_recipe is not None:
                recipe_list.append(new_recipe)
            i += 1
            
        with open(pickle_recipes, 'wb') as outfile:
            pickle.dump(recipe_list, outfile)

    else:
        with open(pickle_recipes, 'rb') as infile:
            recipe_list = pickle.load(infile)
        print('Loaded recipes')

    # Get all unique ingredients
    unique_ingredients = set()
    for recipe in recipe_list:
        unique_ingredients.update(list(recipe.ingredients.keys()))
    unique_ingredients = sorted(unique_ingredients)
    
    for recipe in recipe_list:
        recipe.set_ingredients(unique_ingredients)

    recipes_ingredients_matrix = utils.get_recipes_ingredients_matrix(recipe_list, len(unique_ingredients))
    

    #####################################################################
    #####################################################################
    #####################################################################


    # TODO: maybe just delete this if the sklearn thig works
    """def nearest_neighbor_update(matrix, iterations=100, learning_rate=0.1):
        num_points = matrix.shape[0]
        
        for _ in range(iterations):
            # Calculate pairwise Euclidean distances between points using broadcasting
            distances = np.linalg.norm(matrix[:, np.newaxis, :] - matrix, axis=2)
            
            # Set diagonal elements to infinity to exclude self-distances
            np.fill_diagonal(distances, np.inf)
            
            # Find the index of the nearest neighbor for each point
            nearest_neighbors = np.argmin(distances, axis=1)
            
            # Update each point towards its nearest neighbor
            for i in range(num_points):
                neighbor_index = nearest_neighbors[i]
                direction = matrix[neighbor_index] - matrix[i]
                matrix[i] += learning_rate * direction
                
        return matrix

    # FIXME: havent actually checked if this works, run some tests
    def cosine_similarity_neighbors(matrix):
        num_points = matrix.shape[0]
        #calculate the cosine similarity for all pts
        cos_sim = cosine_similarity(matrix, complete_matrix)
        #use the highest similarty as the index for the nearest neighbor
        nearest_neighbors_indices = np.argmax(cos_sim, axis=1)
        #run nearest neigbor for the whole matrix
        for i in range(num_points):
            direction = matrix[nearest_neighbors_indices] - matrix[i]
            matrix[i] += learning_rate * direction
            

        for i, idx in enumerate(nearest_neighbors_indices):
            matrix[i][np.isnan(matrix[i])] = complete_matrix[idx][np.isnan(matrix[i])]
        return matrix

    # FIXME: we haven't integrated this function for the user class yet 
    def fill_missing_values_with_avg_nearest_neighbors_from_set(incomplete_matrix, complete_matrices, k=5):
        # Replace NaN values with zeros (or any other value)
        incomplete_matrix[np.isnan(incomplete_matrix)] = 0

        # Initialize list to store nearest neighbor distances and indices
        all_distances = []
        all_indices = []

        # Compute nearest neighbors for each complete matrix
        for complete_matrix in complete_matrices:
            nn = NearestNeighbors(n_neighbors=k)
            nn.fit(complete_matrix)
            distances, indices = nn.kneighbors(incomplete_matrix)
            all_distances.append(distances)
            all_indices.append(indices)

        # Replace NaN values in incomplete matrix with average of nearest neighbors from each complete matrix
        filled_matrix = incomplete_matrix.copy()
        for i in range(len(filled_matrix)):
            nan_indices = np.isnan(incomplete_matrix[i])
            if np.any(nan_indices):
                avg_values = np.zeros_like(filled_matrix[i][nan_indices], dtype=float)
                for distances, indices in zip(all_distances, all_indices):
                    nearest_neighbors = np.take_along_axis(complete_matrices[0][indices[i], :][:, nan_indices], indices, axis=1)
                    avg_values += np.nanmean(nearest_neighbors, axis=1)
                avg_values /= len(complete_matrices)
                filled_matrix[i][nan_indices] = avg_values

        return filled_matrix"""

    # TODO: create a test set of matricies and initialize a new user to test

    # Create 1000 random users
    user_base = []
    for i in range(100):
        user_base.append(User(unique_ingredients, f'user_{i}', recipe_list))


    def dictionary_user_scores():
        # I don't completely remember the purpose of this dictionary
        # Did we want to know how many users rated each recipe 1-5?
        # Or did we want to know _which_ users rated each recipe 1-5?


        # Get names of all recipes
        key_names = [recipe_list[i].recipe_name for i in range(len(recipe_list))]
        subkey_names = [f"{i} stars" for i in range (1, 6)]   # Ratings given by users

        # This allows us to find how many (or which users) rated each recipe 1-5 stars
        my_dict = {key: {subkey: 0 for subkey in subkey_names} for key in key_names}

        return my_dict
    
    # Initialize recipe scores for each user based on ingredient scores
    for user in user_base:
        user.ingredient_to_recipe_score_conversion(recipe_list)

    users_ingredients_matrix = utils.get_users_ingredients_matrix(user_base, len(unique_ingredients))


    
    #####################################################################
    #####################################################################
    #####################################################################


    user_id = 'Christian'
    christian = User(unique_ingredients, user_id, recipe_list) 

    def find_k_neighbors(user_ingredient_weights, users_ingredients_matrix, num_neighbors=10):
        # Find the k neighbors with the closest ingredeients taste profile to new user
        neighbors = NearestNeighbors()
        neighbors.fit(users_ingredients_matrix)

        ingredients_matrix = np.array(user_ingredient_weights, dtype=float).reshape(1,-1)   # Convert list of ingredient weights to np.array of appropriate size
        nearest_neighbors = neighbors.kneighbors(ingredients_matrix, num_neighbors)[1][0]   # Get just the indices of the nearest neighbors
        return nearest_neighbors
    
    k_neighbors = find_k_neighbors(christian.ingredient_weights, users_ingredients_matrix)

    def update_ingredient_scores(user_ingredient_weights, k_neighbors):
        # Update user's ingredient taste profile to be closer to that of their k nearest neighbors
        neighbors_scores_matrix = user_ingredient_weights
        for i in range(len(k_neighbors)):
            neighbor_scores = user_base[k_neighbors[i]].ingredient_weights
            neighbors_scores_matrix = np.vstack((neighbors_scores_matrix, neighbor_scores))
        updated_scores = np.mean(neighbors_scores_matrix, axis=0)
        return updated_scores

    christian.ingredient_weights = update_ingredient_scores(christian.ingredient_weights, k_neighbors)


    # def nearest_neighbor_update(matrix, iterations=100, learning_rate=0.1):
    #     num_points = matrix.shape[0]
    
    #     for _ in range(iterations):
    #         # Calculate pairwise Euclidean distances between points using broadcasting
    #         distances = np.linalg.norm(matrix[:, np.newaxis, :] - matrix, axis=2)
            
    #         # Set diagonal elements to infinity to exclude self-distances
    #         np.fill_diagonal(distances, np.inf)
            
    #         # Find the index of the nearest neighbor for each point
    #         nearest_neighbors = np.argmin(distances, axis=1)
            
    #         # Update each point towards its nearest neighbor
    #         for i in range(num_points):
    #             neighbor_index = nearest_neighbors[i]
    #             direction = matrix[neighbor_index] - matrix[i]
    #             matrix[i] += learning_rate * direction
                
    #     return matrix
    
    
    # TODO: Use matrix factorization to recommend recipies not tried

    user_id = 'Josh'
    josh = User(unique_ingredients, user_id, recipe_list)
    # print(josh.taste_profile_dict)
    # print('*'*88)
    # print(josh.taste_profile_weights)

    # os.remove(pickle_recipes)

        # TODO: Steps: 
    #   1. Recommend most popular recipe using matrix factorization on the user score set
    #   2. if they spend more than 10 mins on  the recipe page, and no rating given, asssume recipe made and assign score based on ingredient scores
    #   4. Start giving scores for recipes based on user preferences as well as users also liked
    #       - Calcualte ocmpatibility by giving them our predicted score for any given recipe
    #   5. recommend similar reciepes as well  based on similar ingredients
    #       - Identifying main carb or protien then listing as similar
    #   6. 