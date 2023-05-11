#When using map start the virtual env first
#source venv/bin/activate

import folium
from json_parser import read_business_files
from folium.plugins import MarkerCluster



directory = "yelp_files/business/json"
businesses = read_business_files(directory)

# Create list of state abbreviations in America
america_states = ['AL', 'AK', 'AZ', 'AR',
                   'CA', 'CO', 'CT', 'DE', 
                   'FL', 'GA', 'HI', 'ID', 'IL', 
                   'IN', 'IA', 'KS', 'KY', 'LA', 
                   'ME', 'MD', 'MA', 'MI', 'MN', 
                   'MS', 'MO', 'MT', 'NE', 'NV', 
                   'NH', 'NJ', 'NM', 'NY', 'NC', 
                   'ND', 'OH', 'OK', 'OR', 'PA', 
                   'RI', 'SC', 'SD', 'TN', 'TX', 
                   'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']


# Create map
m = folium.Map(location=[37, -95], zoom_start=4.5, tiles="cartodb positron")


# # Create marker cluster with max zoom of 10
marker_cluster = MarkerCluster(max_zoom=10).add_to(m)


# Add markers for the first 10 businesses
num_businesses = 10

for i in range(num_businesses):
    business = businesses[i]

    if business.state in america_states:
    
        # Extract location data
        lat = business.latitude
        lon = business.longitude
    
        # Create marker and add to map
        folium.Marker([lat, lon], popup=business.name).add_to(marker_cluster)




# Save map to HTML file
m.save("Businesses.html")


