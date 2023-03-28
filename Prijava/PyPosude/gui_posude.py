import tkinter as tk
from tkinter import ttk
from database import *
from crud import *
from PyPosude.crud_posude import CreateNewContainerScreen
from PyPosude.detalji_posude import ContainerDetails
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

class ContainersScreen(ttk.Frame):
    def __init__(self, parent, session):
        super().__init__(parent)
        self.winfo_parent = parent
        self.session = session
        self.notebook = ttk.Notebook(self)
        

        self.label = ttk.LabelFrame(self, text="Containers Screen")
        self.label.grid(padx=10, pady=10)

        self.canvas = tk.Canvas(self.label, highlightthickness=0, height=500, width=640)
        self.canvas.grid(sticky='nsew')

        scrollbar_y = ttk.Scrollbar(self.label, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        self.canvas.config(yscrollcommand=scrollbar_y.set)

        scrollbar_x = ttk.Scrollbar(self.label, orient=tk.HORIZONTAL, command=self.canvas.xview)
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        self.canvas.config(xscrollcommand=scrollbar_x.set)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.container_labelframes = []
        self.add_container_button = ttk.Button(
            self.label, 
            text="Dodaj novu \nPyPosudu", 
            command=self.get_container_details)
        self.add_container_button.grid(row=1, column=2, sticky='ne')

        refresh_button = ttk.Button(self.label, text="Refresh", command=self.refresh_screen)
        refresh_button.grid(row=0, column=2)

        self.create_container_labelframes()

    def create_container_labelframes(self, containers=[]):
        # Loop through each container and create a corresponding LabelFrame
        for container in containers:
            # Create a LabelFrame for the container
            lf_container = ttk.LabelFrame(self.container_labelframes, text=f"Container {container.container_id}")
            lf_container.pack(pady=5)

            # Create a LabelFrame for the associated plant (if any)
            lf_plant = ttk.LabelFrame(lf_container, text="Plant Information")
            lf_plant.pack(pady=5)

            # Get the associated plant (if any)
            plant = container.plant

            # If there is an associated plant, display its name and descriptions
            if plant:
                ttk.Label(lf_plant, text=f"Name: {plant.plant_name}").pack(anchor='w', padx=5, pady=2)
                ttk.Label(lf_plant, text=f"Description 1: {plant.plant_description_one}").pack(anchor='w', padx=5, pady=2)
                ttk.Label(lf_plant, text=f"Description 2: {plant.plant_description_two}").pack(anchor='w', padx=5, pady=2)
            else:
                ttk.Label(lf_plant, text="No plant associated with this container.").pack(anchor='w', padx=5, pady=2)

            # Display information about the container itself
            ttk.Label(lf_container, text=f"Location: {container.container_location}").pack(anchor='w', padx=5, pady=2)
            ttk.Label(lf_container, text=f"Material: {container.container_material}").pack(anchor='w', padx=5, pady=2)

            # Create a LabelFrame for the sensors associated with the container
            lf_sensors = ttk.LabelFrame(lf_container, text="Sensor Readings")
            lf_sensors.pack(pady=5)

            # Get the sensors associated with the container and display their readings
            sensors = container.sensors
            if not sensors:
                ttk.Label(lf_sensors, text="No sensors associated with this container.").pack(anchor='w', padx=5, pady=2)
            else:
                for sensor in sensors:
                    ttk.Label(lf_sensors, text=f"Sensor Type: {sensor.sensor_type}").pack(anchor='w', padx=5, pady=2)
                    ttk.Label(lf_sensors, text=f"Moisture: {sensor.moisture}").pack(anchor='w', padx=5, pady=2)
                    ttk.Label(lf_sensors, text=f"Light: {sensor.light}").pack(anchor='w', padx=5, pady=2)
                    ttk.Label(lf_sensors, text=f"Soil: {sensor.soil}").pack(anchor='w', padx=5, pady=2)

        # Update the container_labelframes list
        self.container_labelframes = [lf for lf in self.label.winfo_children() if isinstance(lf, ttk.LabelFrame)]

    def refresh_screen(self):
        # Clear the existing container labelframes
        for labelframe in self.container_labelframes:
            labelframe.destroy()

        # Recreate the container labelframes
        self.create_container_labelframes()

    def get_container_details(self, container_id):
        container_details_window = tk.Toplevel(self.winfo_parent)
        container_details_window.title(f"Container {container_id} Details")

        container_details = ContainerDetails(container_details_window, container_id, self.session)
        container_details.grid(row=0, column=0)
