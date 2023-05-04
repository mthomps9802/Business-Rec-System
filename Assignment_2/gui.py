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
        for b in cluster:
            similarity_score = round(1 - get_cosine_similarity(b, medoid), 2)
            output_text.insert(tk.END, f'\t- {b.name} ({b.business_id}) - Similarity Score: {similarity_score}\n')
        output_text.insert(tk.END, '\n')



class Gui:
    def __init__(business, master):
        business.master = master
        business.master.title('Business Cluster Generator')

        #Num Drop List
        k_label = ttk.Label(master, text= 'Select k:')
        k_label.pack(padx=10, pady=10, anchor=tk.W)
        business.k_var = tk.IntVar()
        business.k_var.set(1)
        k_menu = ttk.OptionMenu(master, business.k_var, 1, *[i for i in range(1, 16)])
        k_menu.pack(padx=10, pady=10, anchor=tk.W)

        #Generate clusters button
        generate_button = ttk.Button(master, text='Generate Clusters', command = business.generate_clusters)
        generate_button.pack(padx=10, pady=10)

        #Text Box
        business.output_text = tk.Text(master, height= 25, width=110)
        business.output_text.pack(padx=10, pady=10)


    def generate_clusters(business):
        #Get k
        k = business.k_var.get()
        #Generate the clusters
        clusters = k_medoids(businesses, k)
        #Output the clusters
        business.output_text.delete(1.0, tk.END)
        clustersOutput(clusters, business.output_text)

root= tk.Tk()
gui = Gui(root)
root.mainloop()
#k = 5       
#clusters = k_medoids(businesses, k)
#clustersOutput(clusters)




