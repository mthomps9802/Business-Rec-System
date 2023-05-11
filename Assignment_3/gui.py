from json_parser import read_business_files
from k_medoids import k_medoids
from similarity import get_cosine_similarity
import tkinter as tk
from tkinter import ttk

directory_path = directory = "../BusinessRec/yelp_files/business/json/"
businesses = read_business_files(directory)

# Get the clusters using the k-medoids algorithm          
def clustersOutput(clusters, output_text):
    for i, cluster in enumerate(clusters):
        medoid = min(cluster, key=lambda b: sum(1 - get_cosine_similarity(b, other_b) for other_b in cluster))
        output_text.insert(tk.END, f'\nCluster {i+1}:\n')
        output_text.insert(tk.END, f'Medoid: {medoid.name}\n')
        output_text.insert(tk.END, 'Businesses:\n')
        counter = 0
        for b in cluster:
            similarity_score = round(1 - get_cosine_similarity(b, medoid), 2)
            output_text.insert(tk.END, f'\t- {b.name}  - Similarity Score: {similarity_score}\n')
            counter +=1
            if counter == 5:
                break
        output_text.insert(tk.END, '\n')



# Set up the GUI
root = tk.Tk()
root.title("Business Recommender")

# Add a frame for the business list
list_frame = ttk.Frame(root)
list_frame.pack(side=tk.LEFT, fill=tk.Y)

# Scrollbar for the business list
list_scrollbar = ttk.Scrollbar(list_frame)
list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Listbox for the businesses
business_listbox = tk.Listbox(list_frame, yscrollcommand=list_scrollbar.set,height = 40 ,width=40)
for business in businesses:
    business_listbox.insert(tk.END, business.name)
business_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
list_scrollbar.config(command=business_listbox.yview)

root.mainloop()

#k = 5       
#clusters = k_medoids(businesses, k)
#clustersOutput(clusters)




