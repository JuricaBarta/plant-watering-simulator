import tkinter as tk
from tkinter import ttk
from database import *
from crud import *


class CreateNewContainerScreen(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Kreiraj novu posudu")
        self.geometry("400x300")

        # create two LabelFrames
        self.list_containers_frame = ttk.LabelFrame(self, text="Popis posuda")
        self.list_containers_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.options_frame = ttk.LabelFrame(self, text="Opcije")
        self.options_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # add a Listbox to list_containers_frame
        self.listbox = tk.Listbox(self.list_containers_frame, height=10)
        self.listbox.pack(fill="both", expand=True)

        # populate the Listbox with containers
        self.populate_containers_listbox()

        # add Buttons to options_frame
        self.add_buttons()

    def populate_containers_listbox(self):
        # get all containers from the database
        containers = session.query(Container).all()

        # clear the Listbox
        self.listbox.delete(0, "end")

        # repopulate the Listbox with the updated list of containers
        for container in containers:
            self.listbox.insert("end", f"{container.container_id} - {container.container_material}")

    def add_buttons(self):
        for child in self.options_frame.winfo_children():
            child.destroy()

        button_add = ttk.Button(
            self.options_frame,
            text="Dodaj novu posudu",
            command=self.add_new_container
        )
        button_add.pack(pady=10)

        button_update = ttk.Button(
            self.options_frame,
            text="Ažuriraj postojeću posudu",
            command=self.update_existing_container
        )
        button_update.pack(pady=10)

        button_delete = ttk.Button(
            self.options_frame,
            text="Izbriši posudu",
            command=self.remove_container
        )
        button_delete.pack(pady=10)

        # add padding to all widgets in options_frame
        for child in self.options_frame.winfo_children():
            child.pack_configure(padx=5, pady=5)

    def add_new_container(self):
        # clear the options_frame and create entry and button widgets
        for child in self.options_frame.winfo_children():
            child.destroy()

        name_label = ttk.Label(self.options_frame, text="Ime/materijal posude:")
        name_label.pack(pady=10)

        name_entry = ttk.Entry(self.options_frame)
        name_entry.pack(pady=5)

        location_label = ttk.Label(self.options_frame, text="Lokacija posude:")
        location_label.pack(pady=10)

        location_entry = ttk.Entry(self.options_frame)
        location_entry.pack(pady=5)

        save_button = ttk.Button(
            self.options_frame,
            text="Spremi posudu",
            command=lambda: self.submit_container(name_entry.get(), location_entry.get()),
        )
        save_button.pack(pady=10)

    def submit_container(self, name, container_location):
        container_id = get_next_container_id()  # You need to implement this function
        plant_id = container_id
        create_container(name, container_location, plant_id)
        print(f"Uspješno ste pohranili posudu {name} u bazu podataka")
        self.update_containers_listbox()
        self.add_buttons()

    def generate_unique_plant_id():
        # Implement a function to generate a unique plant_id
        pass

    def update_containers_listbox(self):
        # get all containers from the database
        containers = session.query(Container).all()

        # clear the Listbox
        self.listbox.delete(0, "end")

        # repopulate the Listbox with the updated list of containers
        for container in containers:
            self.listbox.insert("end", f"{container.container_id} - {container.container_material}")

    def remove_container(self):
        # get the selected container from the Listbox
        selected_container = self.listbox.get(self.listbox.curselection()[0])

        # get the ID of the selected container from the Listbox
        container_id = selected_container.split("-")[0].strip()

        # delete the selected container from the database
        delete_container(session, int(container_id))

        # delete the selected container from the Listbox
        self.listbox.delete(tk.ACTIVE)

        print(f"Posuda {selected_container} je uspješno izbrisan iz baze podataka.")

    def update_existing_container(self):
        # get the selected container from the Listbox
        selected_container = self.listbox.get(self.listbox.curselection()[0])

        # get the ID and name of the selected container from the Listbox
        container_id, container_material = selected_container.split("-")
        container_id = container_id.strip()

        # clear the options_frame and create entry and button widgets
        for child in self.options_frame.winfo_children():
            child.destroy()

        name_label = ttk.Label(self.options_frame, text="Ime posude:")
        name_label.pack(pady=10)

        name_entry = ttk.Entry(self.options_frame)
        name_entry.pack(pady=5)

        save_button = ttk.Button(
            self.options_frame, 
            text="Spremi promjene", 
            command=lambda: self.update_container(
                int(container_id),
                name_entry.get() or None
            )
        )

        save_button.pack(pady=10)

        # pre-fill the Entry widgets with the current container data
        container = session.query(Container).get(int(container_id))
        name_entry.insert(0, container.container_material)

    def update_container(self, container_id, container_material=None):
        # update the selected container in the database
        container = session.query(Container).get(container_id)
        
        if container_material is not None:
            container.container_material = container_material

        session.commit()
