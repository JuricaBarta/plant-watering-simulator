import tkinter as tk
from tkinter import ttk
from crud import *
from biljke.crud_bilja import CreateNewPlantScreen
from PIL import Image, ImageTk


class PlantsScreen(tk.Frame):
    def __init__(self, parent, notebook):
        tk.Frame.__init__(self, parent)
        self.notebook = notebook
        
        self.label = tk.LabelFrame(self, text="Plants Screen")
        self.label.grid(padx=10, pady=10)

        self.canvas = tk.Canvas(self.label, highlightthickness=0, width=500, height=500)
        self.canvas.grid(sticky='nsew')

        scrollbar = tk.Scrollbar(self.label, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.canvas.config(yscrollcommand=scrollbar.set)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        # Create Refresh button to "reupload" pictures if needed
        self.refresh_button = tk.Button(self.label, text="Refresh", command=self.update_plant_labelframes)
        self.refresh_button.grid(row=0, column=2, sticky=tk.NE)

        """# Create new button that opens new gui window where plants can be created etc.
        self.plant_labelframes = []
        self.add_plant_button = tk.Button(self.label, text="Dodaj novu biljku", command=self.show_new_plant_screen)
        self.add_plant_button.grid(row=1, column=2, sticky=tk.E, columnspan=2)


        self.view_details_button = tk.Button(self.label, text="View Details", command=self.switch_to_plant_details)
        self.view_details_button.grid(row=2, column=2, sticky=tk.NS)


        self.create_plant_labelframes()

        self.frame.bind('<Configure>', self.on_frame_configure)


    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def create_plant_labelframes(self):
        self.plant_names = [
            'Acer', 'Anthurium', 'Bamboo',
            'Calla', 'Davallia Fejeensis',
            'Dracena Marginata', 'Epipremnum',
            'Monstera Deliciosa', 'Pillea Elefantore',
            'Spatifilum'
        ]

        self.plant_images = [
            'acer.jpg', 'anthurium.jpg', 'bamboo.jpg',
            'calla.jpg', 'davallia_fejeensis.jpg', 'dracena_marginata.jpg',
            'epipremnum.jpg', 'pillea_elefantore.jpg',
            'monstera_deliciosa.jpg', 'spatifilum.jpg'
        ]

        for i, plant_name in enumerate(self.plant_names):
            column = i % 2
            row = i // 2

            labelframe_plant = tk.LabelFrame(self.frame)
            labelframe_plant.grid(row=row, column=column, padx=10, pady=10)

            plant_label = tk.Label(labelframe_plant)
            plant_picture_in = PlantImage(self.plant_images[i])
            plant_label['image'] = plant_picture_in.get_plant_images_by_plant_id()
            plant_label.grid(row=0, column=0)

            plant_name_label = tk.Label(labelframe_plant, text=f"{plant_name} Plant")
            plant_name_label.grid(row=1, column=0, pady=10, padx=10)

            self.plant_labelframes.append(labelframe_plant)

    def show_new_plant_screen(self):
        new_plant_screen = CreateNewPlantScreen()
        new_plant = new_plant_screen.add_buttons()

        if new_plant:
            for i, labelframe in enumerate(self.plant_labelframes):
                plant_name_label = labelframe.grid_slaves(row=1, column=0)[0]
                if not plant_name_label.cget('text'):
                    self.plant_names[i] = new_plant[0]
                    self.plant_images[i] = new_plant[1]
                    self.update_plant_labelframe(i, *new_plant)
                    break


    def update_plant_labelframe(self, index, plant_name, plant_image):
        labelframe_plant = self.plant_labelframes[index]
        plant_label = labelframe_plant.grid_slaves(row=0, column=0)[0]
        current_image = plant_label.cget('image').filename
        if plant_image != current_image:
            plant_picture = PlantImage(plant_image)
            plant_label.config(image=plant_picture.get_image())
        plant_name_label = labelframe_plant.grid_slaves(row=1, column=0)[0]
        plant_name_label.config(text=f"{plant_name} Plant")"""


    def update_plant_labelframes(self):
        # Remove existing plant labels
        self.frame.destroy()

        # Recreate the plant labels based on updated plant data
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')
        self.create_plant_labelframes()

        # Update the layout
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def show_new_plant_screen(self):
        new_plant_screen = CreateNewPlantScreen()
        new_plant = new_plant_screen.add_buttons()

        if new_plant:
            plant_name, plant_image = new_plant
            self.plant_names.append(plant_name)
            self.plant_images.append(plant_image)
            self.create_plant_labelframes()
            self.canvas.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def switch_to_plant_details(self):
        self.notebook.select(3)
