import json

class Business:

    def __init__(self, business_id, name,state, address, latitude, longitude, review_count):
        self.business_id = business_id
        self.name = name
        self.categories = None
        self.state = state
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.review_count = review_count
    
    def __str__(self):
        return f"Business(business_id={self.business_id}, categories={self.categories}, name={self.name}, state={self.state}, address={self.address}, latitude={self.latitude}, longitude={self.longitude}, review_count={self.review_count})"
    
    def __repr__(self):
        return self.__str__()
    

    def to_json(self):
        return json.dumps(self.__dict__)
    
    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
    
        return Business(data['business_id'], data['name'], data['state'], data['address'],
                        data['latitude'], data['longitude'], data['review_count'])
        
