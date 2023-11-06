import tkinter as tk
from tkinter import ttk
from database import Plant, session
from crud import create_plant, delete_plant


class CreateNewPlantScreen(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Kreiraj novu biljku")
        self.geometry("400x300")

        # create two LabelFrames
        self.list_plants_frame = ttk.LabelFrame(self, text="Popis biljaka")
        self.list_plants_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.options_frame = ttk.LabelFrame(self, text="Opcije")
        self.options_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # add a Listbox to list_plants_frame
        self.listbox = tk.Listbox(self.list_plants_frame, height=10)
        self.listbox.pack(fill="both", expand=True)

        # populate the Listbox with plants
        self.populate_plants_listbox()

        # add Buttons to options_frame
        self.add_buttons()

    def populate_plants_listbox(self):
        # get all plants from the database
        plants = session.query(Plant).all()

        # clear the Listbox
        self.listbox.delete(0, "end")

        # repopulate the Listbox with the updated list of plants
        for plant in plants:
            self.listbox.insert("end", f"{plant.plant_id} - {plant.plant_name}")

    def add_buttons(self):
        for child in self.options_frame.winfo_children():
            child.destroy()

        button_add = ttk.Button(
            self.options_frame, 
            text="Dodaj novu biljku", 
            command=self.add_new_plant
            )
        button_add.pack(pady=10)

        button_update = ttk.Button(
            self.options_frame, 
            text="Ažuriraj postojeću biljku",
            command=self.update_existing_plant
            )
        button_update.pack(pady=10)

        button_delete = ttk.Button(
            self.options_frame, 
            text="Izbriši biljku", 
            command=self.remove_plant
            )
        button_delete.pack(pady=10)

        # add padding to all widgets in options_frame
        for child in self.options_frame.winfo_children():
            child.pack_configure(padx=5, pady=5)

    def add_new_plant(self):
        # clear the options_frame and create entry and button widgets
        for child in self.options_frame.winfo_children():
            child.destroy()

        name_label = ttk.Label(self.options_frame, text="Ime biljke:")
        name_label.pack(pady=10)

        name_entry = ttk.Entry(self.options_frame)
        name_entry.pack(pady=5)

        image_label = ttk.Label(self.options_frame, text="Naziv slike (opcionalno):")
        image_label.pack(pady=10)

        image_entry = ttk.Entry(self.options_frame)
        image_entry.pack(pady=5)

        save_button = ttk.Button(
            self.options_frame, 
            text="Spremi biljku", 
            command=lambda: self.submit_plant(name_entry.get(), 
            image_entry.get() or None)
            )
        save_button.pack(pady=10)

    def submit_plant(self, name, image):
        create_plant(name, image)
        print(f"Uspješno ste pohranili biljku {name} u bazu podataka")
        self.update_plants_listbox()
        self.add_buttons()

    def update_plants_listbox(self):
        # get all plants from the database
        plants = session.query(Plant).all()

        # clear the Listbox
        listbox = self.list_plants_frame.winfo_children()[0]
        listbox.delete(0, "end")

        # repopulate the Listbox with the updated list of plants
        for plant in plants:
            listbox.insert("end", f"{plant.plant_id} - {plant.plant_name}")


    def remove_plant(self):
    # get the selected plant from the Listbox
        self.listbox = self.list_plants_frame.winfo_children()[0]
        selected_plant = self.listbox.get(self.listbox.curselection()[0])

        # get the ID of the selected plant from the Listbox
        plant_id = selected_plant.split("-")[0].strip()

        # delete the selected plant from the database
        delete_plant(session, int(plant_id))

        # delete the selected plant from the Listbox
        self.listbox.delete(tk.ACTIVE)

        print(f"Biljka {selected_plant} je uspješno izbrisana iz baze podataka.")
        

    def update_existing_plant(self):
        # get the selected plant from the Listbox
        listbox = self.list_plants_frame.winfo_children()[0]
        selected_plant = listbox.get(listbox.curselection()[0])

        # get the ID and name of the selected plant from the Listbox
        plant_id, plant_name = selected_plant.split("-")
        plant_id = plant_id.strip()

        # clear the options_frame and create entry and button widgets
        for child in self.options_frame.winfo_children():
            child.destroy()

        name_label = ttk.Label(self.options_frame, text="Ime biljke:")
        name_label.pack(pady=10)

        name_entry = ttk.Entry(self.options_frame)
        name_entry.pack(pady=5)

        desc1_label = ttk.Label(self.options_frame, text="Opis biljke 1:")
        desc1_label.pack(pady=10)

        desc1_entry = ttk.Entry(self.options_frame)
        desc1_entry.pack(pady=5)

        desc2_label = ttk.Label(self.options_frame, text="Opis biljke 2:")
        desc2_label.pack(pady=10)

        desc2_entry = ttk.Entry(self.options_frame)
        desc2_entry.pack(pady=5)

        save_button = ttk.Button(
            self.options_frame, 
            text="Spremi promjene", 
            command=lambda: self.update_plant(
                int(plant_id),
                name_entry.get() or None,
                desc1_entry.get(),
                desc2_entry.get() or None
            )
        )

        save_button.pack(pady=10)

        # pre-fill the Entry widgets with the current plant data
        plant = session.query(Plant).get(int(plant_id))
        name_entry.insert(0, plant.plant_name)
        if plant.plant_description_one is not None and plant.plant_description_one != "":
            desc1_entry.insert(0, plant.plant_description_one)
        if plant.plant_description_two is not None and plant.plant_description_two != "":
            desc2_entry.insert(0, plant.plant_description_two)


    def update_plant(self, plant_id, plant_name=None, plant_description_one=None, plant_description_two=None):
        # update the selected plant in the database
        plant = session.query(Plant).get(plant_id)

        if plant_name is not None:
            plant.plant_name = plant_name

        if plant_description_one is not None:
            plant.plant_description_one = plant_description_one

        if plant_description_two is not None:
            plant.plant_description_two = plant_description_two

        session.commit()
<<<<<<< Updated upstream
=======

    def submit_plant_and_create_labelframe(self, name_entry, image_entry):
        # Get the plant name and image from the Entry widgets
        name = name_entry.get()
        image = image_entry.get() or None

        # Call the submit_plant function
        self.submit_plant(name, image)

        # Call the create_new_labelframe function
        self.create_new_labelframe(name, image)


    """def create_new_labelframe(self, name, image):
        plant_name = name  # You can change this if needed
        plant_image = image  # You can specify the image file if needed
        create_new_labelframe(self.options_frame, plant_name, plant_image)"""
>>>>>>> Stashed changes
