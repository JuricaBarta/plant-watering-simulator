import tkinter as tk
from database import *
from crud import *
from biljke.crud_bilja import CreateNewPlantScreen
from PIL import Image, ImageTk



class PlantsScreen(tk.Frame):
    def __init__(self, parent, main_screen):
        super().__init__(parent)
        self.main_screen = main_screen

        self.label = tk.LabelFrame(self, text="Plants Screen")
        self.label.grid(padx=10, pady=10)

        self.canvas = tk.Canvas(self.label, highlightthickness=0, width=500, height=500)
        self.canvas.grid(sticky='nsew')

        scrollbar = tk.Scrollbar(self.label, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.canvas.config(yscrollcommand=scrollbar.set)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.plant_labelframes = []
        self.add_plant_button = tk.Button(self.label, text="Dodaj novu biljku", command=self.show_new_plant_screen)
        self.add_plant_button.grid(row=1, column=2, sticky='ne')

            # Add the Refresh button
        self.refresh_button = tk.Button(self.label, text="Refresh", command=self.update_plant_labelframes)
        self.refresh_button.grid(row=0, column=2, sticky='nw')


        self.create_plant_labelframes()

        self.frame.bind('<Configure>', self.on_frame_configure)


    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def create_plant_labelframes(self):
        # Fetch plant data from the database, including plant images
        plants = session.query(Plant).all()

        for i, plant in enumerate(plants):
            column = i % 2
            row = i // 2

            labelframe_plant = tk.LabelFrame(self.frame)
            labelframe_plant.grid(row=row, column=column, padx=10, pady=10)

            plant_label = tk.Button(labelframe_plant, command=lambda plant=plant: self.switch_to_tab4(plant))

            # Query associated PlantImage objects for the current plant
            plant_images = plant.plant_images  # Use the relationship directly

            if plant_images:
                first_plant_image = plant_images[0]
                image_filename = first_plant_image.image_path

                # Create an instance of your PlantImage class and get the resized image
                plant_picture = PlantImage(image_filename).open_and_resize()

                if plant_picture:
                    plant_label.config(image=plant_picture)
                    plant_label.image = plant_picture  # Keep a reference to prevent garbage collection
                else:
                    # Handle the case where no plant images are associated with the plant
                    # You can set a default image or display a placeholder here
                    pass
            else:
                # Handle the case where no plant images are associated with the plant
                # You can set a default image or display a placeholder here
                pass

            plant_label.grid(row=0, column=0)

            plant_name_label = tk.Label(labelframe_plant, text=plant.plant_name + " Plant")
            plant_name_label.grid(row=1, column=0, pady=10, padx=10)

            self.plant_labelframes.append(labelframe_plant)

    def switch_to_tab4(self, plant_id):
        self.main_screen.switch_to_tab4(plant_id)


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
        plant_name_label.config(text=f"{plant_name} Plant")

    def update_plant_labelframes(self):
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

    def add_plant_labelframe(self, plant_name, plant_image=None):
        column = len(self.plant_labelframes) % 2
        row = len(self.plant_labelframes) // 2

        labelframe_plant = tk.LabelFrame(self.frame)
        labelframe_plant.grid(row=row, column=column, padx=10, pady=10)

        if plant_image:
            # For existing plants with images, create a button with the existing behavior
            plant_label = tk.Button(labelframe_plant, command=lambda: self.switch_to_tab4())
        else:
            # For new plants without images, define a custom behavior here
            plant_label = tk.Button(labelframe_plant, command=lambda plant_name=plant_name: self.custom_command(plant_name))

        if plant_image:
            plant_picture_in = PlantImage(plant_image)
            plant_label['image'] = plant_picture_in.get_image()

        plant_label.grid(row=0, column=0)

        plant_name_label = tk.Label(labelframe_plant, text=f"{plant_name} Plant")
        plant_name_label.grid(row=1, column=0, pady=10, padx=10)

        self.plant_labelframes.append(labelframe_plant)

    def custom_command(self, plant_name):
    # Define the custom behavior for the new plants here
        print(f"Custom command for {plant_name}")
    # You can add code to switch to a different tab or perform any other action as needed

    def remove_plant_labelframe(self, index):
        if index < len(self.plant_labelframes):
            self.plant_labelframes[index].destroy()
            del self.plant_labelframes[index]

    def create_new_labelframe(self):
        plant_name = "New Plant"  # You can change this default name
        plant_image = None  # You can specify the image file if needed
        self.add_plant_labelframe(plant_name, plant_image)

