from freqTable import FrequencyTable
from business import Business
import json
from typing import List
from collections import defaultdict
import tkinter as tk




def read_business_file(file_path: str) -> List[Business]:
    businesses = []
    business_names = set()
    with open(file_path, 'r') as f:
        counter = 0
        for line in f:
            if counter >= 10000:
                break
            data = json.loads(line)
            business_name = data['name']
            #Checking for duplicate business names
            #if business_name in business_names:
            #    continue
            business = Business(
                data['business_id'], 
                business_name, 
                data['address'], 
                data['city'], 
                data['state'], 
                data['stars'], 
                data['review_count'], 
                data['categories']
            )
            for category in business.categories.split(", "):
                business.ft.add(category)
            businesses.append(business)
            business_names.add(business_name)
            counter += 1
    return businesses

businesses = read_business_file('yelp_files/business.json')

def get_similar_businesses(business: Business, businesses: List[Business]) -> List[Business]:
    similarity_scores = defaultdict(int)
    for other_business in businesses:
        if other_business == business:
            continue
        if business.city == other_business.city or business.state == other_business.state:
            for category in business.categories.split(", "):
                similarity_scores[other_business] += other_business.ft.getCount(category)
    return sorted(similarity_scores.keys(), key=lambda b: similarity_scores[b], reverse=True)



