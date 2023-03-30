
import json

# Open the JSON file and read the first 10000 lines
with open('/Users/mxrksworld/Downloads/BusinessRec/yelp_files/business.json', 'r') as f:
    data = []
    for i in range(10000):
        line = f.readline()
        if not line:
            break
        data.append(json.loads(line))

# Check if the data was read correctly
if data:
    print("Data was read successfully.")
else:
    print("Error reading data.")

# Create a list of business names and categories
business_sim = [(item['name'], item['categories']) for item in data]

# Write the business names and categories to a file in a structured representation
with open('/Users/mxrksworld/Downloads/BusinessRec/yelp_files/business_SimData.txt', 'w') as f:
    for name, categories in business_sim:
        f.write('- Name: {}\n'.format(name))
        f.write('  Categories: {}\n'.format(categories))
