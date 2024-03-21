"""Here we will write the algorthm for finding nearest neighbor Maybe we cna find the 5 closest and take the average of those then updade with that"""
import numpy as np

def nearest_neighbor_update(matrix, iterations=100, learning_rate=0.1):
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


if __name__ == "__main__":

    # Example usage
    initial_matrix = np.array([[1., 2.], [3., 4.], [5., 6.]])
    updated_matrix = nearest_neighbor_update(initial_matrix)
    print("Updated matrix:")
    print(updated_matrix)