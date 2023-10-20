from tkinter import ttk, Label
from biljke.crud_bilja import CreateNewPlantScreen
from crud import *
from database import *
from PIL import Image, ImageTk

class PlantDetails(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.plants = session.query(Plant).all()
        self.plants_list = self.plants[:]  # Create a list to store all plants
        self.current_plant_index = 0

        # configure the grid to have two columns
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1) 

        self.plant_image_label = Label(self, image=None)
        self.plant_image_label.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.label = ttk.LabelFrame(self, text="Plant Details")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.plant_picture = ttk.Label(self.label)
        self.plant_picture.grid(row=0, column=0, padx=10, pady=10)

        self.plant_name_label = ttk.Label(self.label, text="")
        self.plant_name_label.grid(row=1, column=0, padx=10, pady=10)

        self.plant_description_label = ttk.Label(self.label, text="", anchor="w")
        self.plant_description_label.grid(row=2, column=0, padx=10, pady=10)

        button_previous_plant = ttk.Button(self, text="Previous Plant", command=self.previous_plant)
        button_previous_plant.grid(row=3, column=0, padx=10, pady=10, sticky="w") 

        button_next_plant = ttk.Button(self, text="Next Plant", command=self.next_plant)
        button_next_plant.grid(row=3, column=1, padx=10, pady=10, sticky="e")  

        button_open_creator_window = ttk.Button(self, text="Dodaj novu biljku", command=self.open_creator_window)
        button_open_creator_window.grid(row=4, column=1, padx=10, pady=10, sticky="e")

        # display the first plant
        self.display_plant()

    def display_plant(self, current_plant=None, plant_images=None):
        if current_plant:
            # Fetch the image path for the current plant from associated PlantImage
            if plant_images:
                plant_image_path = plant_images[0].image_path 

                # Display the image of the current plant
                if plant_image_path:
                    plant_image = Image.open(plant_image_path)
                    plant_image = plant_image.resize((250, 250), Image.ANTIALIAS)
                    plant_image_tk = ImageTk.PhotoImage(plant_image)
                    self.plant_image_label.configure(image=plant_image_tk)
                    self.plant_image_label.image = plant_image_tk
                else:
                    self.plant_image_label.configure(text="No Image")
            else:
                self.plant_image_label.configure(text="No Image")

            # Display the name and description of the current plant
            self.plant_name_label.configure(text=current_plant.plant_name)

            descriptions = [
                desc for desc in [
                    current_plant.plant_description_one,
                    current_plant.plant_description_two,
                    current_plant.plant_description_three,
                    current_plant.plant_description_four
                ] if desc is not None  
            ]

            if not any(descriptions):
                self.plant_description_label.configure(text="No more info about the plant")
            else:
                self.plant_description_label.configure(text="\n".join(descriptions))


    def add_new_plant(self):
        name = "New Plant" 
        image = None  
        create_plant(name, image)

        new_plant = session.query(Plant).filter_by(plant_name=name).first()
        self.plants_list.append(new_plant)

    def next_plant(self):
        if self.current_plant_index < len(self.plants_list) - 1:
            self.current_plant_index += 1
            self.display_plant()


    def previous_plant(self):
        if self.current_plant_index > 0:
            self.current_plant_index -= 1
            self.display_plant()

    def open_creator_window(self):
        create_new_plant_screen = CreateNewPlantScreen()
        create_new_plant_screen.grid(row=4, column=0, padx=10, pady=10)
