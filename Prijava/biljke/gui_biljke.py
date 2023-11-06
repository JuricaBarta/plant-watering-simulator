import tkinter as tk
from database import *
from crud import *
from biljke.crud_bilja import CreateNewPlantScreen


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

<<<<<<< Updated upstream
            # Add the Refresh button
        self.refresh_button = tk.Button(self.label, text="Refresh", command=self.update_plant_labelframes)
=======
        #self.add_image_button = tk.Button(self.label, text="Dodaj novu sliku", command=self.upload_and_display_image)
        #self.add_image_button.grid(row=1, column=0, sticky='nw')

        self.refresh_button = tk.Button(self.label, text="Refresh", command=self.create_plant_labelframes)
>>>>>>> Stashed changes
        self.refresh_button.grid(row=0, column=2, sticky='nw')

        self.create_plant_labelframes()

        self.frame.bind('<Configure>', self.on_frame_configure)


    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

<<<<<<< Updated upstream
=======
    def switch_to_tab4(self, current_plant):
        tab4 = self.main_screen.notebook.nametowidget(self.main_screen.notebook.tabs()[3])

        # Fetch associated PlantImage objects for the selected plant
        plant_images = current_plant.plant_images

        if plant_images:
            self.main_screen.notebook.select(3)
            tab4.display_plant(current_plant, plant_images)

    # Remove the plant_button_click function
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
            plant_label = tk.Button(labelframe_plant, command=lambda: self.switch_to_tab4())

            plant_picture_in = PlantImage(self.plant_images[i])
            plant_label['image'] = plant_picture_in.get_image()
            plant_label.grid(row=0, column=0)

            plant_name_label = tk.Label(labelframe_plant, text=f"{plant_name} Plant")
            plant_name_label.grid(row=1, column=0, pady=10, padx=10)
=======
            plant_images = plant.plant_images

            # Create a flag to check if the plant image is available
            has_plant_image = bool(plant_images)

            # Initialize plant_picture as None
            plant_picture = None

            if has_plant_image:
                first_plant_image = plant_images[0]
                image_filename = first_plant_image.image_path

                # Create an instance of your PlantImage class and get the resized image
                plant_picture = PlantImage(image_filename).open_and_resize()

            # Create the plant label button for switching to Tab 4
            switch_to_tab4_button = tk.Button(labelframe_plant, text="Switch to Tab 4", command=lambda plant=plant: self.switch_to_tab4(plant))
            switch_to_tab4_button.grid(row=0, column=0)

            # Create the plant label button for uploading an image
            upload_image_button = tk.Button(labelframe_plant, text="Upload Photo", command=lambda plant=plant, frame=labelframe_plant: self.upload_and_display_image(plant, frame))
            upload_image_button.grid(row=1, column=0)

            if plant_picture:
                switch_to_tab4_button.config(image=plant_picture)
                switch_to_tab4_button.image = plant_picture

            plant_name_label = tk.Label(labelframe_plant, text=plant.plant_name + " Plant")
            plant_name_label.grid(row=2, column=0, pady=10, padx=10)

            self.plant_labelframes.append(labelframe_plant)



            if plant_picture:
                switch_to_tab4_button.config(image=plant_picture)
                switch_to_tab4_button.image = plant_picture

            plant_name_label = tk.Label(labelframe_plant, text=plant.plant_name + " Plant")
            plant_name_label.grid(row=2, column=0, pady=10, padx=10)
>>>>>>> Stashed changes

            self.plant_labelframes.append(labelframe_plant)

    def switch_to_tab4(self):
        self.main_screen.switch_to_tab4()


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

<<<<<<< Updated upstream

=======
    def upload_and_display_image(self, current_plant, labelframe):
        # Open a file dialog for image selection
        f_types = [("Jpg files", "*.jpg"), ("PNG files", "*.png")]
        filename = filedialog.askopenfilename(filetypes=f_types)

        if filename:
            # Load the selected image and display it in the label
            img = Image.open(filename)
            img = img.resize((150, 200))
            img = ImageTk.PhotoImage(img)
            image_label = labelframe.grid_slaves(row=0, column=0)[0]
            image_label.config(image=img)
            image_label.image = img

            # Set the flag to indicate that the plant now has an image
            current_plant.has_plant_image = True

    def custom_command(self, plant_name):
        print(f"Custom command for {plant_name}")

    def remove_plant_labelframe(self, index):
        if index < len(self.plant_labelframes):
            self.plant_labelframes[index].destroy()
            del self.plant_labelframes[index]

    def create_new_labelframe(self):
        plant_name = "New Plant"
        plant_image = None

        column = len(self.plant_labelframes) % 2
        row = len(self.plant_labelframes) // 2

        labelframe_plant = tk.LabelFrame(self.frame)
        labelframe_plant.grid(row=row, column=column, padx=10, pady=10)

        # Create the plant label button for uploading an image
        upload_image_button = tk.Button(labelframe_plant, text="Upload Photo", command=lambda plant=plant, frame=labelframe_plant: self.upload_and_display_image(plant, frame))
        upload_image_button.grid(row=0, column=0)


        plant_name_label = tk.Label(labelframe_plant, text=f"{plant_name} Plant")
        plant_name_label.grid(row=1, column=0, pady=10, padx=10)

        self.plant_labelframes.append(labelframe_plant)
>>>>>>> Stashed changes
