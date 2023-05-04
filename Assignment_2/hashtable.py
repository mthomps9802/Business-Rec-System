import json
import hashlib


# Define the maximum number of records per block
MAX_RECORDS_PER_BLOCK = 10000

# Define the hash function to use
HASH_FUNCTION = hashlib.sha256

# Define the path to the Yelp businesses file
BUSINESSES_FILE = "/Users/mxrksworld/Downloads/BusinessRec/yelp_files/business.json"

# Define the path to the hash table file
HASH_TABLE_FILE = "/Users/mxrksworld/Downloads/BusinessRec/Assignment_2/hashtable.txt"

# Create an empty hash table file if it doesn't exist
try:
    with open(HASH_TABLE_FILE, "r") as f:
        hash_table = json.load(f)
except FileNotFoundError:
    hash_table = {}
    with open(HASH_TABLE_FILE, "w") as f:
        json.dump(hash_table, f)

# Open the Yelp businesses file
with open(BUSINESSES_FILE, "r") as f:
    businesses = json.load(f)

# Define the block class
class Block:
    def __init__(self, block_num):
        self.block_num = block_num
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def remove_record(self, record):
        self.records.remove(record)

    def is_full(self):
        return len(self.records) >= MAX_RECORDS_PER_BLOCK

    def write_to_file(self):
        block_filename = f"block{self.block_num}.json"
        block_path = f"/Users/mxrksworld/Downloads/BusinessRec/yelp_rec/blocks/{block_filename}"
        with open(block_path, "w") as f:
            json.dump(self.records, f)
        hash_table[self.block_num] = block_filename
        with open(HASH_TABLE_FILE, "w") as f:
            json.dump(hash_table, f)

# Define the hash function
def hash_business(business):
    hash_obj = HASH_FUNCTION()
    hash_obj.update(business["name"].encode())
    hash_obj.update(business["city"].encode())
    hash_obj.update(business["state"].encode())
    return hash_obj.digest()

# Create an empty buffer cache
buffer_cache = {}

# Process each Yelp business
for business in businesses:
    # Calculate the hash value of the business
    hash_value = hash_business(business)
    block_num = int.from_bytes(hash_value[:2], byteorder="big") % 10
    # Check if the block exists
    if block_num in hash_table:
        # Read the block from disk or cache
        block_filename = hash_table[block_num]
        if block_filename in buffer_cache:
            block = buffer_cache[block_filename]
        else:
            block_path = f"/Users/mxrksworld/Downloads/BusinessRec/yelp_rec/blocks/{block_filename}"
            
            with open(block_path, "r") as f:
                block = Block(block_num)
                block.records = json.load(f)
            buffer_cache[block_filename] = block
        # Check if the business already exists in the block
        for record in block.records:
            if record["name"] == business["name"] and record["city"] == business["city"] and record["state"] == business["state"]:
                # Update the existing record
                record["filename"] = business["filename"]
                block.write_to_file()
                break
        else:
            # Add the new record to the block
            if block.is_full():
                # Create a new block if the current one is full
                block = Block(len(hash_table) + 1)
                buffer_cache[f"block{block.block_num}.json"] = block
            block.add_record({"name": business["name"], "city": business["city"], "state": business["state"]})
