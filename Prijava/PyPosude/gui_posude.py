import tkinter as tk
from tkinter import ttk
from database import Base, engine, session, Plant, PlantImage, Sensor, Container
from crud import PlantImage, generate_sensor_data
from PyPosude.crud_posude import CreateNewContainerScreen
from PyPosude.detalji_posude import ContainerDetails
#from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

class ContainersScreen(ttk.Frame):
    def __init__(self, parent, session):
        super().__init__(parent)
        self.winfo_parent = parent
        self.session = session
        self.notebook = ttk.Notebook(self)

        self.label = tk.LabelFrame(self, text="Containers Screen")
        self.label.grid(padx=10, pady=10)

        self.canvas = tk.Canvas(self.label, highlightthickness=0, height=500, width=640)
        self.canvas.grid(sticky='nsew')

        scrollbar_y = tk.Scrollbar(self.label,  orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        self.canvas.config(yscrollcommand=scrollbar_y.set)

        scrollbar_x = tk.Scrollbar(self.label, orient=tk.HORIZONTAL, command=self.canvas.xview)
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        self.canvas.config(xscrollcommand=scrollbar_x.set)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.container_labelframes = []
        self.add_container_button = tk.Button(
            self.label, 
            text="Dodaj novu \nPyPosudu", 
            command=self.show_container_details)
        self.add_container_button.grid(row=1, column=2, sticky='ne')

        refresh_button = tk.Button(self.label, text="Refresh", command=self.refresh_screen)
        refresh_button.grid(row=0, column=2)

        self.create_container_labelframes()

        self.frame.bind('<Configure>', self.on_frame_configure)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def create_container_labelframes(self):
        self.plant_names = [
            'Acer', 'Anthurium', 'Bamboo'
        ]

        self.plant_images = [
            'acer.jpg', 'anthurium.jpg', 'bamboo.jpg'
        ]

        for i, plant_name in enumerate(self.plant_names):
            column = i % 2
            row = i // 2

            labelframe_container = tk.LabelFrame(self.frame)
            labelframe_container.grid(row=row, column=column, padx=10, pady=10)

            container_label = tk.Label(labelframe_container)
            plant_picture_in = PlantImage(self.plant_images[i])
            container_label['image'] = plant_picture_in.get_image()
            container_label.grid(row=0, column=0, padx=10, pady=10)

            container_name_label = tk.Label(labelframe_container, text=f"{plant_name} Plant")
            container_name_label.grid(row=1, column=0, pady=10, padx=10)

            container_id = i + 1

            sensor_info = self.generate_sensor_data(container_id)


            sensor_label = tk.Label(labelframe_container, text=sensor_info)
            sensor_label.grid(row=0, column=1, padx=10, pady=10)

            view_details_button = tk.Button(
                labelframe_container,
                text="View Details", 
                command=lambda container_id=container_id: self.show_container_details(container_id)
                )
            view_details_button.grid(row=1, column=1, pady=10)
            
    def generate_sensor_data(self, container_id):
        # Create a new session
        session = Session()

        # Get the container with the specified ID
        container = session.query(Container).filter(Container.container_id == container_id).first()

        # Initialize the sensor information string
        sensor_info = ""

        # Loop over all sensors in the container
        for sensor in container.sensors:
            # Add the location of the sensor to the sensor information string
            sensor_info += f"Location: {sensor.sensor_location}\n"
            
            # Check if the sensor has a moisture reading and add it to the sensor information string
            if sensor.moisture is not None:
                sensor_info += f"Moisture reading: {sensor.moisture:.2f}\n"
            
            # Check if the sensor has a light reading and add it to the sensor information string
            if sensor.light is not None:
                sensor_info += f"Light reading: {sensor.light}\n"
            
            # Add the substrate recommendation to the sensor information string
            sensor_info += f"Substrate recommendation:\n {sensor.substrate_recommendation}\n\n"

        # Close the session
        session.close()

        # Return the sensor information string
        return sensor_info

    def show_container_details(self, container_id):
        container_details = ContainerDetails(self.notebook, session=self.session, container_id=container_id)
        self.notebook.add(container_details, text=f"Detalji posude {container_id}")
        self.notebook.select(container_details) 

        # Get the notebook widget
        notebook = self.master.nametowidget(self.master.winfo_parent())

        # Select the tab with index 1 (i.e., tab2)
        notebook.select(1)

        # Get the instance of the ContainerDetails class and update its details
        container_details_screen = self.master.nametowidget(self.master.winfo_children()[1])
        container_details_screen.show_container_details(container_details_screen)
        container_details_screen = ContainerDetails(self.master, self.session, container_id=Container)

    def show_new_container_screen(self):
        create_new_container_screen = CreateNewContainerScreen(self.master)
        create_new_container_screen.grid()

    def refresh_screen(self):
        for labelframe in self.container_labelframes:
            labelframe.destroy()

        self.container_labelframes = []
        self.create_container_labelframes()
