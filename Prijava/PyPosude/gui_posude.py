import requests
import tkinter as tk
from tkinter import ttk
from crud import PlantImage, generate_sensor_readings, generate_readings
from PyPosude.crud_posude import CreateNewContainerScreen
from PyPosude.detalji_posude import ContainerDetails
import random 

class ContainersScreen(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = tk.LabelFrame(self, text="Containers Screen")
        self.label.grid(padx=10, pady=10)

        self.canvas = tk.Canvas(self.label, highlightthickness=0, height=500, width=640)
        self.canvas.grid(sticky='nsew')

        scrollbar = tk.Scrollbar(self.label,  orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.canvas.config(yscrollcommand=scrollbar.set)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.container_labelframes = []
        self.add_container_button = tk.Button(self.label, text="Dodaj novu PyPosudu", command=self.show_new_container_screen)
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
            container_label.grid(row=0, column=0)
        

            container_name_label = tk.Label(labelframe_container, text=f"{plant_name} Plant")
            container_name_label.grid(row=1, column=0, pady=10, padx=10)

            container_sensors = tk.Label(labelframe_container)
            #sensor_in_label = generate_readings(sensor_type='')
            #container_sensors['sensor'] =  sensor_in_label.generate_sensor_readings()
            container_sensors.grid(row=0, column=1, pady=10, padx=10)

            """container_id = i + 1
            sensors = generate_sensor_readings(container_id)

            if sensors:
                sensor_info = "Sensors: "
                for sensor in sensors:
                    sensor_info += f"{sensor.sensor_type} ({sensor.sensor_location}), "

                # Remove the trailing comma and space
                sensor_info = sensor_info[:-2]
            else:
                sensor_info = "No sensors found."

            container_sensors.config(text=sensor_info)

            view_details_button = tk.Button(labelframe_container, text="View Details", command=lambda container_id=container_id: self.show_container_details(container_id))
            view_details_button.grid(row=1, column=1, pady=10)"""

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

