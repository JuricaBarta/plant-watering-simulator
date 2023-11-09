import tkinter as tk
from tkinter import ttk
from database import Plant, session
from crud import create_plant, delete_plant


class CreateNewPlantScreen(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Kreiraj novu biljku")
        self.geometry("400x700")

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
        # Clear the options_frame and create entry and button widgets
        for child in self.options_frame.winfo_children():
            child.destroy()

        name_label = ttk.Label(self.options_frame, text="Ime biljke:")
        name_label.pack(pady=10)

        name_entry = ttk.Entry(self.options_frame)
        name_entry.pack(pady=5)

        description_label = ttk.Label(self.options_frame, text="Opis biljke (opcionalno):")
        description_label.pack(pady=10)

        description_entry = ttk.Entry(self.options_frame)
        description_entry.pack(pady=5)

        moisture_label = ttk.Label(self.options_frame, text="Vlažnost (opcionalno):")
        moisture_label.pack(pady=10)

        moisture_entry = ttk.Entry(self.options_frame)
        moisture_entry.pack(pady=5)

        light_label = ttk.Label(self.options_frame, text="Svjetlo i temperatura (opcionalno):")
        light_label.pack(pady=10)

        light_entry = ttk.Entry(self.options_frame)
        light_entry.pack(pady=5)

        substrate_label = ttk.Label(self.options_frame, text="Podloga (opcionalno):")
        substrate_label.pack(pady=10)

        substrate_entry = ttk.Entry(self.options_frame)
        substrate_entry.pack(pady=5)

        save_button = ttk.Button(
            self.options_frame, 
            text="Spremi biljku", 
            command=lambda: self.submit_plant(
                name_entry.get(), 
                description_entry.get() or None, 
                moisture_entry.get() or None, 
                light_entry.get() or None, 
                substrate_entry.get() or None
            )
        )
        save_button.pack(pady=10)

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
        # Get the selected plant from the Listbox
        listbox = self.list_plants_frame.winfo_children()[0]
        selected_plant = listbox.get(listbox.curselection()[0])

        # Get the ID and name of the selected plant from the Listbox
        plant_id, plant_name = selected_plant.split("-")
        plant_id = plant_id.strip()

        # Clear the options_frame and create entry and button widgets
        for child in self.options_frame.winfo_children():
            child.destroy()

        name_label = ttk.Label(self.options_frame, text="Ime biljke:")
        name_label.pack(pady=10)

        name_entry = ttk.Entry(self.options_frame)
        name_entry.pack(pady=5)

        desc_label = ttk.Label(self.options_frame, text="Opis biljke:")
        desc_label.pack(pady=10)

        desc_entry = ttk.Entry(self.options_frame)
        desc_entry.pack(pady=5)

        moisture_label = ttk.Label(self.options_frame, text="Moisture info (opcionalno):")
        moisture_label.pack(pady=10)

        moisture_entry = ttk.Entry(self.options_frame)
        moisture_entry.pack(pady=5)

        light_temp_label = ttk.Label(self.options_frame, text="Light and temperature info (opcionalno):")
        light_temp_label.pack(pady=10)

        light_temp_entry = ttk.Entry(self.options_frame)
        light_temp_entry.pack(pady=5)

        substrates_label = ttk.Label(self.options_frame, text="Substrates info (opcionalno):")
        substrates_label.pack(pady=10)

        substrates_entry = ttk.Entry(self.options_frame)
        substrates_entry.pack(pady=5)

        save_button = ttk.Button(
            self.options_frame, 
            text="Spremi promjene", 
            command=lambda: self.update_plant(
                int(plant_id),
                name_entry.get() or None,
                desc_entry.get(),
                moisture_entry.get() or None,
                light_temp_entry.get() or None,
                substrates_entry.get() or None
            )
        )

        save_button.pack(pady=10)

        # Pre-fill the Entry widgets with the current plant data
        plant = session.query(Plant).get(int(plant_id))
        name_entry.insert(0, plant.plant_name)
        desc_entry.insert(0, plant.plant_description)

        # Fill the moisture, light, and substrate info if available
        if plant.moisture_info:
            moisture_entry.insert(0, plant.moisture_info)
        if plant.light_temp_info:
            light_temp_entry.insert(0, plant.light_temp_info)
        if plant.substrates:
            substrates_entry.insert(0, plant.substrates)



    def update_plant(self, plant_id, plant_name=None, plant_description=None, moisture_info=None, light_temp_info=None, substrates=None):
        # Update the selected plant in the database
        plant = session.query(Plant).get(plant_id)

        if plant_name is not None:
            plant.plant_name = plant_name

        if plant_description is not None:
            plant.plant_description = plant_description

        if moisture_info is not None:
            plant.moisture_info = moisture_info

        if light_temp_info is not None:
            plant.light_temp_info = light_temp_info

        if substrates is not None:
            plant.substrates = substrates

        session.commit()


    def submit_plant(self, name, description, moisture_info, light_temp_info, substrates):
        create_plant(name, description, moisture_info, light_temp_info, substrates)
        print(f"Uspješno ste pohranili biljku {name} u bazu podataka")
        # After creating the plant, add it to the list of plants and update the UI
        self.update_plants_listbox()
        self.create_new_labelframe(name, description)

    def create_plant(name, description, moisture_info, light_temp_info, substrates):
        # Create an instance of the Plant model and populate its attributes
        plant = Plant(
            plant_name=name,
            plant_description=description,
            moisture_info=moisture_info,
            light_temp_info=light_temp_info,
            substrates=substrates
        )

        # Add the plant instance to the session and commit the changes
        session.add(plant)
        session.commit()


    def create_new_labelframe(self, name, image):
        plant_name = name  # You can change this if needed
        plant_image = image  # You can specify the image file if needed
        #create_new_labelframe(self.options_frame, plant_name, plant_image)