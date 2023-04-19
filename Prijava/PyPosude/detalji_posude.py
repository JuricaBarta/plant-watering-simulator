import tkinter as tk
from tkinter import ttk, Label
from crud import *
from database import *

class ContainerDetails(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        

        self.plant_image_label = Label(self, image=None)
        self.plant_image_label.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.label = tk.LabelFrame(self, text="Container Details")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.plant_picture = tk.Label(self.label)
        self.plant_picture.grid(row=0, column=0, padx=10, pady=10)

        self.plant_name_label = tk.Label(self.label, text="")
        self.plant_name_label.grid(row=1, column=0, padx=10, pady=10)

        self.plant_description_label = tk.Label(self.label, text="", anchor="w")
        self.plant_description_label.grid(row=2, column=0, padx=10, pady=10)

        button_previous_plant = tk.Button(self, text="Previous Plant", command=self.previous_plant)
        button_previous_plant.grid(row=3, column=0, padx=10, pady=10, sticky="w")  

        button_next_plant = tk.Button(self, text="Next Plant", command=self.next_plant)
        button_next_plant.grid(row=3, column=1, padx=10, pady=10, sticky="e")

        self.plants = session.query(Plant).all()
        self.current_plant_index = 0

        self.display_plant()

    def display_plant(self):
        # display the image of the current plant
        plant_image_path = plant_image_names[self.current_plant_index]
        plant_image = Image.open(plant_image_path)
        plant_image = plant_image.resize((250, 250), Image.ANTIALIAS)
        plant_image_tk = ImageTk.PhotoImage(plant_image)
        self.plant_image_label.configure(image=plant_image_tk)
        self.plant_image_label.image = plant_image_tk

        # display the name and sensors of the current container/plant
        self.plant_name_label.configure(text=self.plants[self.current_plant_index].plant_name)

    def next_plant(self):
        # go to the next plant and display it
        if self.current_plant_index < len(self.plants) - 1:
            self.current_plant_index += 1
            self.display_plant()

    def previous_plant(self):
        # go to the previous plant and display it
        if self.current_plant_index > 0:
            self.current_plant_index -= 1
            self.display_plant()

    def show_container_details(self, containers):
        for container in containers:
            container_name_label = ttk.Label(self, text=f"Container Name: {container['name']}")
            container_name_label.pack()
            plant_name_label = ttk.Label(self, text=f"Plant Name: {container['plant']}")
            plant_name_label.pack()
            for sensor in container['sensors']:
                sensor_type_label = ttk