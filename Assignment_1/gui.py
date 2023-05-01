import tkinter as tk
from tkinter import ttk
from businessFunctions import get_similar_businesses
from business import Business
from businessFunctions import businesses



def display_similar_businesses(business: Business):
    similar_businesses = get_similar_businesses(business, businesses)
    text_widget.delete('1.0', tk.END)
    text_widget.insert(tk.END, f'Similar businesses for {business.name}:\n')
    #Changes the amount of recommended businesses
    for i, b in enumerate(similar_businesses[:5]):
        text_widget.insert(tk.END, f'{i + 1}. {b.name}\n')

# Set up the GUI
root = tk.Tk()
root.title("Business Recommender")

# Add a frame for the business list
list_frame = ttk.Frame(root)
list_frame.pack(side=tk.LEFT, fill=tk.Y)

# Add a scrollbar for the business list
list_scrollbar = ttk.Scrollbar(list_frame)
list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Add a listbox for the businesses
business_listbox = tk.Listbox(list_frame, yscrollcommand=list_scrollbar.set, width=30)
for business in businesses:
    business_listbox.insert(tk.END, business.name)
business_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
list_scrollbar.config(command=business_listbox.yview)

# Add a frame for the results
result_frame = ttk.Frame(root)
result_frame.pack(side=tk.LEFT, fill=tk.Y)

# Add a label for the results
result_label = ttk.Label(result_frame, text="Similar businesses:")
result_label.pack(side=tk.TOP, pady=10)

# Add a text widget for the results
text_widget = tk.Text(result_frame, height=20, width=50)
text_widget.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10)

# Add a function to display similar businesses when a business is selected
def display_similar():
    selected = business_listbox.curselection()
    if selected:
        business = businesses[selected[0]]
        display_similar_businesses(business)

# Add a button to display similar businesses
show_button = ttk.Button(result_frame, text="Show similar businesses", command=display_similar)
show_button.pack(side=tk.BOTTOM, pady=10)

# Start the GUI main loop
root.mainloop()
