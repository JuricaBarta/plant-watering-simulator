import tkinter as tk
from tkinter import ttk
from database import Plant, session
from crud import create_plant, update_plant, delete_plant


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
        listbox = tk.Listbox(self.list_plants_frame, height=10)
        listbox.pack(fill="both", expand=True)

        # populate the Listbox with plants
        plants = session.query(Plant).all()
        for plant in plants:
            listbox.insert("end", f"{plant.plant_id} - {plant.plant_name}")

        # add Buttons to options_frame
        self.add_buttons()

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
        selected_plant_id = selected_plant.split("-")[0].strip()

        # delete the selected plant from the database
        delete_plant(selected_plant_id)

        # delete the selected plant from the Listbox
        self.listbox.delete(tk.ACTIVE)

        print(f"Biljka {selected_plant} je uspješno izbrisana iz baze podataka.")

    def update_existing_plant(self):
    # get the selected plant from the Listbox
        self.listbox = self.list_plants_frame.winfo_children()[0]
        selection = self.listbox.get(self.listbox.curselection()[0])
        if not selection:
            return

        selected_plant_str = self.listbox.get(selection[0])
        selected_plant_id = selected_plant_str.split("-")[0].strip()

        # retrieve the selected plant from the database
        selected_plant = session.query(Plant).filter_by(plant_id=selected_plant_id).first()

        # clear the options_frame and create entry and button widgets
        for child in self.options_frame.winfo_children():
            child.destroy()

        name_label = ttk.Label(self.options_frame, text="Ime biljke:")
        name_label.pack(pady=10)

        name_entry = ttk.Entry(self.options_frame)
        name_entry.insert(0, selected_plant.plant_name)
        name_entry.pack(pady=5)

        image_label = ttk.Label(self.options_frame, text="Naziv slike (opcionalno):")
        image_label.pack(pady=10)

        image_entry = ttk.Entry(self.options_frame)
        image_entry.insert(0, selected_plant.image_name or "")
        image_entry.pack(pady=5)

        save_button = ttk.Button(
            self.options_frame, 
            text="Spremi biljku", 
            command=lambda: self.update_plant(selected_plant_id, name_entry.get(), 
            image_entry.get() or None)
            )
        save_button.pack(pady=10)

    def update_plant(self, plant_id, name, image_name):
        # update the selected plant in the database
        session.query(Plant).filter_by(plant_id=plant_id).update({
            "plant_name": name,
            "image_name": image_name
        })
        session.commit()

        # update the Listbox with the updated plant
