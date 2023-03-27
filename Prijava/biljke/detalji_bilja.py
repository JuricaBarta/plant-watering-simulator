import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from database import Plant, Container, session
from crud import *

class PlantDetails(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        # create widgets for displaying plant details
        self.plant_image_label = tk.Label(self, width=200, height=200)
        self.plant_image_label.pack(side=tk.LEFT, padx=10, pady=10)
        self.plant_name_label = tk.Label(self, text="", font=("Arial", 20, "bold"))
        self.plant_name_label.pack(side=tk.TOP, padx=10, pady=10)
        self.plant_desc_label = tk.Label(self, text="")
        self.plant_desc_label.pack(side=tk.LEFT, padx=10, pady=10)

    def show_plant(self, plant):
        # update the plant details labels with the selected plant's info
        self.plant_image_label.config(image=plant.image)
        self.plant_image_label.image = plant.image
        self.plant_name_label.config(text=plant.name)
        self.plant_desc_label.config(text=plant.description)

    def populate_plant_listbox(self):
        self.plants = create_plant() # get the list of plant objects
        for plant in self.plants:
            self.listbox.insert(tk.END, plant.name)

        # bind the listbox selection event to a method
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

    def on_select(self, event):
        # get the selected plant from the listbox
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            plant = self.plants[index]
            self.show_plant(plant)
