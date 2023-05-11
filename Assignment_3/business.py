import json

class Business:

    def __init__(self, business_id, name, state, address, latitude, longitude):
        self.business_id = business_id
        self.name = name
        self.state = state
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.categories = None
        self.neighbors = None
    
    def __repr__(self):
        return f"Business({self.business_id}, {self.name}, {self.latitude}, {self.longitude})"
    
    def __repr__(self):
        return self.__str__()
    

    def to_json(self):
        return json.dumps(self.__dict__)
    
    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
    
        return Business(data['business_id'], data['name'], data['state'], data['address'],
                        data['latitude'], data['longitude'])
        
