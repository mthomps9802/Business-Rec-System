import math
from business import Business

def get_cosine_similarity(business1, business2):
    """
    Returns the cosine similarity between two Business objects based on their category counters.
    """
    # Get the list of unique category names from both businesses
    categories1 = set(business1.categories.keys())
    categories2 = set(business2.categories.keys())
    unique_categories = categories1.union(categories2)
    
    # Initialize the dot product and magnitudes of both businesses' category vectors
    dot_product = 0
    magnitude1 = 0
    magnitude2 = 0
    
    # Calculate the dot product and magnitudes
    for category in unique_categories:
        count1 = business1.categories.get(category, 0)
        count2 = business2.categories.get(category, 0)
        dot_product += count1 * count2
        magnitude1 += count1**2
        magnitude2 += count2**2
    
    # Calculate the cosine similarity
    similarity = dot_product / (math.sqrt(magnitude1) * math.sqrt(magnitude2))
    
    return similarity



