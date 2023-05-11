import os
import json
from haversine import haversine
from json_parser import read_business_files

businesses = read_business_files("yelp_files/business/json")

def get_closest_neighbors(businesses):
    neighbors_dict = {}
    for business1 in businesses:
        closest_neighbors = []
        for business2 in businesses:
            if business1 != business2:
                distance = haversine((business1.latitude, business1.longitude), 
                                     (business2.latitude, business2.longitude))
                closest_neighbors.append((business2, distance))
        closest_neighbors.sort(key=lambda x: x[1])
        neighbors_dict[business1] = closest_neighbors[:4]
    return neighbors_dict

# Example usage
neighbors_dict = get_closest_neighbors(businesses)
print(neighbors_dict)
