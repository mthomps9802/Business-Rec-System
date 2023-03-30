
#Import Statements
import json
import math
import tkinter as tk
from tkinter import messagebox

class FrequencyTable:
    #Initializes new Frequency table
    def __init__(business):
        business.ft = {}
        
    #If the word is in ft its count goes up
    def add(business, word):
        if word not in business.ft:
            business.ft[word] = 1
        else:
            business.ft[word] += 1
            
    #returns the word in the dictionary of the business object 
    def get(business, word):
        if word in business.ft:
            return business.ft[word]
        else:
            return 0

    #returns the total count of all words
    def total(business):
        return sum(business.ft.values())

    #returns count for the word given
    def getCount(business, word):
        return business.get(word)

    #returns a list of all words in the dictionary of the business object
    def getWords(business):
        return business.ft.keys()
    

class Main():
    #constructor
    def __init__(business):
        #initialized variables
        business.NameToId = {}
        business.IdToCategories = {}
        business.IdToNames = {}
        #Stores unique words in reviews
        business.Values = set()
        business.tf = []
        business.IdToLoc = {}
        business.idf = FrequencyTable()
        #Method calls
        business.read_data() #Reads data
        business.calculate_frequency_tables() #Calculate Frequency Tables
        business.calculate_tfidf() #Calculate TF-IDF vectors
        
    
    def read_data(business):
        #File path
        file = "/Users/mxrksworld/Downloads/BusinessRec/yelp_files/business.json"
        #Stores the necessary information in its specified variable
        with open(file, "r") as f:
            count = 0
            #for loop to read 10k lines
            for line in f:
                if count >= 10000: #Num of businesses
                    break
                obj = json.loads(line)
                business.NameToId[obj["name"]] = obj["business_id"]
                business.IdToNames[obj["business_id"]] = obj["name"]
                business.IdToCategories[obj["business_id"]] = obj["categories"]
                business.IdToLoc[obj["business_id"]] = len(business.tf)
                business.tf.append(FrequencyTable())
                count += 1
                
    
    #Calculates frequency tables for each business
    def calculate_frequency_tables(business):
        business.tf = [FrequencyTable() for i in range(len(business.NameToId))] #Creates a list freq table for each business
        i = 0
        business.Values.update(business.NameToId.values()) #Sets unique business IDs
        print(business.Values.update(business.NameToId.values())) #Prrints unique business IDs
        for k in business.Values:
            getCategories = business.IdToCategories.get(k)
            #print(getCategories)
            if getCategories is not None:
                for category in getCategories:
                    business.IdToLoc[k] = i  #Set business Index
                    business.tf[i].add(category)
            i += 1
            #print(The tf: ,business.tf)
        for k in business.IdToCategories.keys():
            categories = business.IdToCategories.get(k)
            if categories is not None:
                for category in categories:
                    business.idf.add(category) #Adds category to freq table
                    #print("The idf: ,business.idf)

                    
    #Calculate TF-IDF vectors for every business
    def calculate_tfidf(business):
        num_docs = len(business.tf) 
        for i in range(num_docs):
            for word in business.tf[i].getWords():
                tf = business.tf[i].get(word) #Gets freq of each word 
                idf = business.idf.get(word) #Gets inverse doc freq of each word
                if idf is not None:
                    tfidf = tf * math.log(num_docs / idf) #Calculates tf-idf for current word 
                    business.tf[i].ft[word] = tfidf #Sets tfidf valuue for current word


    #Calculates the TF-IDF vector for the selected business and the
    #cosine similarity between it and other businesses
    def select_action(business):
        selection = business.bus.curselection() 
        if selection:
            # Get the selected business name 
            business_name = business.bus.get(selection[0])
            business_id = business.NameToId[business_name]
            # Calculate the TF-IDF vector for the selected business
            selected_tfidf = business.tf[business.IdToLoc[business_id]]
            # Calculate the cosine similarity between the selected business and all the other businesses
            similarity_scores = {}
            for name, business_id in business.NameToId.items():
                if name == business_name: #Skips business if it shares the same name as what user chose
                    continue
                tfidf = business.tf[business.IdToLoc[business_id]]
                similarity_scores[name] = business.cosine_similarity(selected_tfidf, tfidf) 
            #Find the business with the highest similarity score
            #closest_business = max(similarity_scores, key=similarity_scores.get) #Easier way to get the top recommendation
                 #Sort sim scores in descending order
                #Converts to a list of tuples
            sorted_scores = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
            closest_business = sorted_scores[0][0] #Gets name of business with highest sim
            second_closest_business = sorted_scores[1][0] #Gets name of business with second highest sim
            # Output the closest business in the GUI
            business.outputArea.delete("1.0", tk.END)
            business.outputArea.insert(tk.END, f"Recommended Businesses: \n {closest_business}.\n {second_closest_business}")
            #business.outputArea.insert(tk.END, f"Recommended Business: {second_closest_business}.")



    #Calculates the cosine similarity between two TF-IDF vectors
    def cosine_similarity(business, tfidf1, tfidf2):
        dot_product = 0
        bus1 = 0
        bus2 = 0
        for word in set(tfidf1.getWords()) | set(tfidf2.getWords()):
            dot_product += tfidf1.get(word) * tfidf2.get(word) #Calculate the product between both vectors
            bus1 += tfidf1.get(word) ** 2  #First vector squared sum
            bus2 += tfidf2.get(word) ** 2 #Second vector squared sum
        bus1 = math.sqrt(bus1)
        bus2 = math.sqrt(bus2)
        if bus1 == 0 or bus2 == 0:
            return 0
        return dot_product / (bus1 * bus2) #Cos sim
        


    #GUI 
    def create_gui(business):
        business.frame = tk.Tk()
        business.frame.title("Business Recommendations")
        business.bus = tk.Listbox(business.frame, width=50)
        business.bus.pack(side=tk.LEFT, fill=tk.BOTH)
        #Binds select_action method to list box
        business.bus.bind("<<ListboxSelect>>", lambda x: business.select_action()) 
        scrollbar = tk.Scrollbar(business.frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        business.bus.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=business.bus.yview)
        for item in business.NameToId.keys():
            business.bus.insert(tk.END, item) #Inserts each key as an item in the listbox
        #print("Creating outputArea widget...")
        business.outputArea = tk.Text(business.frame, height=20, width=60)
        business.outputArea.pack(side=tk.RIGHT, fill=tk.BOTH)
        #print("outputArea widget created and packed.")


    #Runs the program by calling the gui and main function
    def run(business):
        business.create_gui()
        business.frame.mainloop()


#Creates an instance of the main class and calls its run method
if __name__ == '__main__':
    main = Main()
    main.run()
