import os
import math
from json_parser import read_business_files


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on the Earth's surface
    using the Haversine formula.
    """
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c


def record_business_links(directory_path):
    businesses = read_business_files(directory_path)

    for business in businesses:
        distances = []
        for other in businesses:
            if business.business_id != other.business_id:
                distance = haversine_distance(
                    business.latitude, business.longitude,
                    other.latitude, other.longitude
                )
                distances.append((other.name, distance))
        distances.sort(key=lambda x: x[1])
        closest = distances[:4]

        dir_path = "yelp_files/recorded_links"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        file_path = f"{dir_path}/{business.name}.txt"
        if not os.path.exists(file_path):
            print(f"{file_path} does not exist. Creating file.")
            with open(file_path, "w") as f:
                f.write(f"Business: {business.name}\n")
                for name, distance in closest:
                    f.write(f"\t- {name}\n")
        else:
            print(f"{file_path} exists. Changes added to file.")
            with open(file_path, "w") as f:
                f.write(f"Business: {business.name}\n")
                for name, distance in closest:
                    f.write(f"\t- {name}\n")

    print("Links recorded successfully.")





directory_path = "/Users/mxrksworld/Downloads/BusinessRec/yelp_files/business/json"

record_business_links(directory_path)