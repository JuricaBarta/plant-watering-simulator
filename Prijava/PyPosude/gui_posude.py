import tkinter as tk
from tkinter import ttk
from crud import *
from PyPosude.crud_posude import CreateNewContainerScreen
from PyPosude.detalji_posude import ContainerDetails
import random 
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

class ContainersScreen(ttk.Frame):
    def __init__(self, parent, main_screen):
        super().__init__(parent)
        self.main_screen = main_screen

        self.label = ttk.LabelFrame(self, text="Containers Screen")
        self.label.grid(padx=10, pady=10)

        self.canvas = tk.Canvas(self.label, highlightthickness=0, height=600, width=640)
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
        self.add_container_button = tk.Button(self.label, text="Dodaj novu PyPosudu", command=self.show_new_container_screen)
        self.add_container_button.grid(row=1, column=2, padx=5, pady=5)

        refresh_button = tk.Button(self.label, text="Refresh", command=self.refresh_screen)
        refresh_button.grid(row=0, column=2, padx=5, pady=5)

        self.open_tab2_button = tk.Button(self.label, text="Open Tab 2", command=lambda: self.switch_to_tab2(container_name=""))
        self.open_tab2_button.grid(row=1, column=1, padx=5, pady=5)

        self.sync_button = tk.Button(self.label, text="SYNC", command=self.sync_sensors)
        self.sync_button.grid(row=1, column=0, padx=5, pady=5)

        self.create_container_labelframes()

        self.frame.bind('<Configure>', self.on_frame_configure)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))


    def create_container_labelframes(self):
        self.plant_names = ['Acer', 'Anthurium', 'Bamboo']
        self.plant_images = ['acer.jpg', 'anthurium.jpg', 'bamboo.jpg']
        sensor_types = ["Moisture", "Light", "Soil"]

        self.sensor_labels = []

        for i, plant_name in enumerate(self.plant_names):
            column = i % 2
            row = i // 2

            labelframe_container = tk.LabelFrame(self.frame)
            labelframe_container.grid(row=row, column=column, padx=10, pady=10)

            button_container = tk.Button(labelframe_container, text=plant_name, command=lambda container_name=plant_name: self.switch_to_tab2(container_name))
            button_container.grid(row=0, column=0)

            plant_picture_in = PlantImage(self.plant_images[i])
            button_container.config(image=plant_picture_in.get_image(), compound=tk.TOP)

            sensor_frame = tk.Frame(labelframe_container)
            sensor_frame.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=10)

            for sensor_type in sensor_types:
                sensor_reading = tk.Label(sensor_frame, text=self.generate_sensor_data(sensor_type))
                sensor_reading.pack(side=tk.TOP, padx=5, pady=5)
                self.sensor_labels.append(sensor_reading)

    def add_sensor(self, sensor_type, container_id):
        # Generate random sensor data
        moisture = random.uniform(0, 100)
        light = random.uniform(0, 10000)
        soil = random.uniform(0, 14)

        create_sensor(sensor_type=sensor_type, container_id=container_id, moisture=moisture, light=light, soil=soil)

    def generate_sensor_data(self, sensor_type, sync=False):
        if not sync:
            if sensor_type == "Moisture":
                return f"Moisture: {random.uniform(0, 100):.2f}%"
            elif sensor_type == "Light":
                return f"Light: {random.uniform(0, 10000):.2f} lm"
            elif sensor_type == "Soil":
                return f"Soil: {random.uniform(0, 14):.1f}ph" 
        else:
            if sensor_type == "Moisture":
                return "Moisture: 40.00%"
            elif sensor_type == "Light":
                return "Light: 5000.00 lm"
            elif sensor_type == "Soil":
                return "Soil: 7.00 ph"
            
    def sync_sensors(self):
        sensor_types = ["Moisture", "Light", "Soil"]
        for i in range(len(self.sensor_labels)):
            if i < len(self.sensor_labels):
                self.sensor_labels[i].configure(text=self.generate_sensor_data(sensor_types[i], sync=True))


            
    def show_container_details(self, container_id):
        container_details_screen = ContainerDetails(self.master, container_id)
        container_details_screen.grid()

    def show_new_container_screen(self):
        create_new_container_screen = CreateNewContainerScreen(self.master)
        create_new_container_screen.grid()

    def refresh_screen(self):
        for labelframe in self.container_labelframes:
            labelframe.destroy()

        self.container_labelframes = []
        self.create_container_labelframes()

    def sync_sensors(self):
        sensor_types = ["Moisture", "Light", "Soil"]
        sensor_index = 0
        for _ in self.plant_names:
            for i in range(len(sensor_types)):
                if sensor_index < len(self.sensor_labels):
                    self.sensor_labels[sensor_index].configure(text=self.generate_sensor_data(sensor_types[i], sync=True))
                    sensor_index += 1
        print ("Containers have been synced, plants are now happy :)")

    def switch_to_tab2(self, container_name):
        container_data = {"name": container_name, "sensors": {}}
        sensors = get_sensor_by_id(container_name)
        for sensor in sensors:
            container_data["sensors"][sensor.sensor_type] = {"reading": sensor.reading, "ideal_reading": sensor.ideal_reading}
        
        self.main_screen.show_tab2(container_data)

