from freqTable import FrequencyTable

class Business:
    def __init__(self, business_id, name, address, city, state, stars, review_count, categories):
        self.business_id = business_id
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.stars = stars
        self.review_count = review_count
        if categories is None:
            categories = ''
        self.categories = categories
        self.ft = FrequencyTable()