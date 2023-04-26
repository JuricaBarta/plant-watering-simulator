from tkinter import ttk, Label
from biljke.crud_bilja import CreateNewPlantScreen
from crud import *
from database import *
from biljke.gui_biljke import *
from PIL import Image, ImageTk


class PlantDetails(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # configure the grid to have two columns
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1) 

        self.plant_image_label = Label(self, image=None)
        self.plant_image_label.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.label = tk.LabelFrame(self, text="Plant Details")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

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

        button_open_creator_window = tk.Button(self, text="Dodaj novu biljku", command=self.open_creator_window)
        button_open_creator_window.grid(row=4, column=1, padx=10, pady=10, sticky="e") 

        # add the plants list and the index of the currently displayed plant
        self.plants = session.query(Plant).all()
        self.current_plant_index = 0

        # display the first plant
        self.display_plant()

    def display_plant(self):
        # display the image of the current plant
        plant_image_path = plant_image_names[self.current_plant_index]
        plant_image = Image.open(plant_image_path)
        plant_image = plant_image.resize((250, 250), Image.ANTIALIAS)
        plant_image_tk = ImageTk.PhotoImage(plant_image)
        self.plant_image_label.configure(image=plant_image_tk)
        self.plant_image_label.image = plant_image_tk

        # display the name and description of the current plant
        self.plant_name_label.configure(text=self.plants[self.current_plant_index].plant_name)
        descriptions = [self.plants[self.current_plant_index].plant_description_one,
                        self.plants[self.current_plant_index].plant_description_two,
                        self.plants[self.current_plant_index].plant_description_three,
                        self.plants[self.current_plant_index].plant_description_four]
        self.plant_description_label.configure(text="\n".join(descriptions))

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


    def open_creator_window(self):
        create_new_plant_screen = CreateNewPlantScreen()
        create_new_plant_screen.grid(row=4, column=0, padx=10, pady=10)
