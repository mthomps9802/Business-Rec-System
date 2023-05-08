import json
import re
from business import Business
from collections import Counter


path_to_business_file = "yelp_files/business.json"
path_to_review_file = "yelp_files/business/json/json"


def get_words(text):
    """
    Returns a list of words extracted from a given text string.
    """
    # Remove all non-alphabetic characters and digits
    text = re.sub(r"[^a-zA-Z ]+", "", text)
    # Split the text into words and return as a list
    return text.split()


import os

def create_business_files(total_files, directory_path):
    file_count = 0
    json_dir = os.path.join(directory_path, "json")
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
    with open(path_to_business_file, "r", encoding="utf-8") as f:
        for line in f:
            if file_count == total_files:
                break
            data = json.loads(line)
            categories = data['categories']
            if categories is not None:
                business = Business.from_json(line)
                business.categories = Counter(get_words(categories))
                categories = data['categories']
                with open(os.path.join(json_dir, f"{business.business_id}.json"), "w") as f:
                    f.write(business.to_json())  
                file_count += 1  


def read_business_files(directory_path):
    businesses = []    
    json_dir = os.path.join(directory_path, "json")
    if not os.path.exists(json_dir):
        return businesses
    for filename in os.listdir(json_dir):
        if filename.endswith(".json"):
            with open(os.path.join(json_dir, filename), "r") as f:
                data = json.load(f)
                business = Business(
                    data['business_id'],
                    data['name'],
                    data['state'],
                    data['address'],
                    data['latitude'],
                    data['longitude'],
                    data['review_count']
                )
                business.categories = Counter(data['categories'])
                businesses.append(business)
    return businesses


#Used to choose the amount of files youd like in the cluster pool
directory = "yelp_files/business/json"
create_business_files(500, directory)


#businesses = read_business_files(directory)
#print(businesses)