from tkinter import ttk, Label
from biljke.crud_bilja import CreateNewPlantScreen
from crud import *
from database import *
from PIL import Image, ImageTk

class PlantDetails(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.plants = session.query(Plant).all()

        # Initialize plants_list with the order you want
        self.plants_list = [plant for plant in self.plants]

        # Initialize the current plant index
        self.current_plant_index = 0

        # Configure the grid to have two columns
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

        # Display the first plant
        self.display_plant()

    def display_plant(self, current_plant=None, plant_images=None):
        if current_plant:
            # Display the name of the current plant
            self.plant_name_label.configure(text=current_plant.plant_name)
            
            descriptions = [
                desc for desc in [
                    current_plant.plant_description,
                    "\n"
                    "Moisture info:",
                    current_plant.moisture_info,
                    "\n",  # Add a line break after Moisture info
                    "Light and temperature info:",
                    current_plant.light_temp_info,
                    "\n",  # Add a line break after Light and temperature info
                    "Substrates info:",
                    current_plant.substrates
                ] if desc is not None
            ]

            # Check if there are any descriptions
            if not any(descriptions):
                self.plant_description_label.configure(text="No more info about the plant")
            else:
                # Use '\n' to separate descriptions for multi-line display
                plant_description = "\n".join(descriptions)
                self.plant_description_label.configure(text=plant_description)

            # Fetch the image path for the current plant from associated PlantImage
            if plant_images:
                plant_image_path = plant_images[0].image_path
                # Do something with the image path, e.g., display the image




                # Display the image of the current plant
                if plant_image_path:
                    plant_image = Image.open(plant_image_path)
                    plant_image = plant_image.resize((250, 250), Image.ANTIALIAS)
                    plant_image_tk = ImageTk.PhotoImage(plant_image)
                    self.plant_image_label.configure(image=plant_image_tk)
                    self.plant_image_label.image = plant_image_tk
                else:
                    self.plant_image_label.configure(image=None)  # Clear the image
                    self.plant_image_label.configure(text="No image")

    def next_plant(self):
        if self.current_plant_index < len(self.plants_list) - 1:
            self.current_plant_index += 1
        current_plant = self.plants_list[self.current_plant_index]
        plant_images = current_plant.plant_images  # Fetch the associated images
        self.display_plant(current_plant, plant_images)

    def previous_plant(self):
        if self.current_plant_index > 0:
            self.current_plant_index -= 1
        current_plant = self.plants_list[self.current_plant_index]
        plant_images = current_plant.plant_images  # Fetch the associated images
        self.display_plant(current_plant, plant_images)

    def open_creator_window(self):
        create_new_plant_screen = CreateNewPlantScreen()
        create_new_plant_screen.grid(row=4, column=0, padx=10, pady=10)