import tkinter as tk
from tkinter import ttk
from crud import create_container
from database import session, Plant, Container

class CreateNewContainerScreen(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Kreiraj novu PyPosudu")
        self.geometry("400x300")

        label = tk.Label(self, text="Tab 2: Kreiranje nove posude")
        label.grid(row=0, column=0, pady=10, padx=10, columnspan=3)
        self.create_container_form()

    def create_container_form(self):
        self.container_frame = tk.LabelFrame(self, text="Add Container")
        self.container_frame.grid(row=1, column=0, padx=10, pady=10, columnspan=3)

        tk.Label(self.container_frame, text="Location").grid(row=0, column=0, padx=10, pady=10)
        self.container_location = tk.Entry(self.container_frame)
        self.container_location.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.container_frame, text="Plant").grid(row=1, column=0, padx=10, pady=10)
        self.container_plant = ttk.Combobox(self.container_frame, values=self.get_plant_names())
        self.container_plant.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.container_frame, text="Add", command=self.add_container).grid(row=2, column=1, padx=10, pady=10)

    def get_plant_names(self):
        plants = session.query(Plant).all()
        return [plant.name for plant in plants]

    def add_container(self):
        plant_name = self.container_plant.get()
        plant = session.query(Plant).filter_by(name=plant_name).first()

        if plant is None:
            plant = Plant(name=plant_name)
            session.add(plant)
            session.commit()

        location = self.container_location.get()
        create_container(location, plant.id)

        self.destroy()

