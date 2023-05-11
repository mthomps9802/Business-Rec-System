import random
from business import Business
from collections import Counter
from similarity import get_cosine_similarity

def k_medoids(businesses, k):
    """
    Clusters a list of Business objects into k clusters using the k-medoids algorithm.
    """
    # Initialize the medoids randomly
    medoids = random.sample(businesses, k)
    
    # Assign each business to the closest medoid
    clusters = [[] for i in range(k)]
    for business in businesses:
        closest_medoid = None
        closest_distance = 0
        for medoid in medoids:
            distance = 1 - get_cosine_similarity(business, medoid)
            if closest_medoid is None or distance < closest_distance:
                closest_medoid = medoid
                closest_distance = distance
        index = medoids.index(closest_medoid)
        clusters[index].append(business)
    
    # Recalculate the medoids by choosing the business with the lowest total distance to other businesses in its cluster
    for i in range(k):
        min_total_distance = None
        new_medoid = None
        for business in clusters[i]:
            total_distance = 0
            for other_business in clusters[i]:
                distance = 1 - get_cosine_similarity(business, other_business)
                total_distance += distance
            if min_total_distance is None or total_distance < min_total_distance:
                min_total_distance = total_distance
                new_medoid = business
        medoids[i] = new_medoid
        
    # Repeat the assignment and recalculation steps until convergence
    while True:
        old_clusters = clusters.copy()
        # Assign each business to the closest medoid
        clusters = [[] for i in range(k)]
        for business in businesses:
            closest_medoid = None
            closest_distance = 0
            for medoid in medoids:
                distance = 1 - get_cosine_similarity(business, medoid)
                if closest_medoid is None or distance < closest_distance:
                    closest_medoid = medoid
                    closest_distance = distance
            index = medoids.index(closest_medoid)
            clusters[index].append(business)
        
        # Check for convergence
        if clusters == old_clusters:
            break
        
        # Recalculate the medoids
        for i in range(k):
            min_total_distance = None
            new_medoid = None
            for business in clusters[i]:
                total_distance = 0
                for other_business in clusters[i]:
                    distance = 1 - get_cosine_similarity(business, other_business)
                    total_distance += distance
                if min_total_distance is None or total_distance < min_total_distance:
                    min_total_distance = total_distance
                    new_medoid = business
            medoids[i] = new_medoid
        
    return clusters



