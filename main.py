import recipe_crawler as rc
from user_class import User
import numpy as np
import pickle
import string
import utils
import time
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors

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
    unique_ingredients = utils.get_unique_ingredients(recipe_list)
    utils.set_ingredients_matrix(recipe_list, unique_ingredients)

    recipes_ingredients_matrix = utils.get_recipes_ingredients_matrix(recipe_list, len(unique_ingredients))
    with open('new_text.txt', 'w') as file:
        np.savetxt(file, recipes_ingredients_matrix)

    # print(recipes_ingredients_matrix)
    user_list = []
    for i in range(10):
        user_list.append(User(unique_ingredients, i, recipe_list))
    

    def dictionary_user_scores():
        key_names = [recipe_list[i].recipe_name for i in range(len(recipe_list))]
        subkey_names = (f"score{i}" for i in range (1,6))

        my_dict = {key: {subkey: 0} for subkey in subkey_names for key in key_names}

        return my_dict


    # print(user_list[0].taste_profile_dict)

    user_ingredient_score = []
    for recipe in recipe_list:
        for user in user_list:
            recipe_score = np.sum(recipe.ingredients_matrix * user.taste_profile_weights) / np.sum(recipe.ingredients_matrix)
            if recipe_score <= 0.2:
                recipe_rating = 1
            elif recipe_score <= 0.4:
                recipe_rating = 2
            elif recipe_score <= 0.6:
                recipe_rating = 3
            elif recipe_score <= 0.8:
                recipe_rating = 4
            else:
                recipe_rating = 5
            
            user.recipe_scores[recipe.recipe_name] = recipe_rating
            # print(user.recipe_scores[recipe.recipe_name]) 

    # print(user_ingredient_score)

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
    
    #create 10000 random users
    userBase = list()
    for i in range(10000):
        userBase.append(np.random.rand((len(unique_ingredients))))
        i += 1

    #make the random taste preferences into a matrix
    user_ingredients_matrix = np.zeros(len(unique_ingredients))   # Placeholder that will be deleted later
    for user in userBase:
        # Create matrix where each row containg the users preference for individual recipes
        user_ingredients_matrix = np.vstack((user_ingredients_matrix, user))

    # Delete the first row of zeros
    user_ingredients_matrix = np.delete(user_ingredients_matrix, (0), axis=0)
    print(user_ingredients_matrix)

    # TODO: If it seems to work for a genral case, brianstorm some edge cases that we can use to AB test the algorithm



    # FIXME: "Learn to use SciKitlearn Cosine similarity and sklearn nearest neighbors, use those instead since they are probably better"
    # TODO: Steps: 
    #   1. Recommend most popular recipe
    #       -most percentage of scores > 3
    #   2. If no rating is given, then look for users who liked the recipe and recommend their top recipe
    #       -Time how long they are on the page, if > x time they made the recipe. If less, they did not makke it
    #       -Take all users who gave recipe 4 or 5 and find all their other 4's and 5's then see what 3 recipies had the most high scores
    #   3. Update according to the nearest 10 of those neighbors
    #   4. Start giving scores for recipes based on user preferences as well as users also liked
    #       - Calcualte ocmpatibility by giving them our predicted score for any given recipe
    #   5. recommend similar reciepes as well  based on similar ingredients
    #       - Identifying main carb or protien then listing as similar





    # USER STUFF
    user_id = 'Christian'
    christian = User(unique_ingredients, user_id, recipe_list) 
    
    user_id = 'Josh'
    josh = User(unique_ingredients, user_id, recipe_list)
    # print(josh.taste_profile_dict)
    # print('*'*88)
    # print(josh.taste_profile_weights)

    # os.remove(pickle_recipes)