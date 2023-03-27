import tkinter as tk
from tkinter import ttk
import matplotlib as mb
#from PyPosude.crud_posude import CreateNewContainerScreen
from PyPosude.gui_posude import *
import matplotlib.pyplot as plt
#from crud import generate_sensor_data
from database import Container

class ContainerDetails(ttk.Frame):
    def __init__(self, parent, session, container_id):
        super().__init__(parent)
        self.session = session
        self.container_id = container_id

        self.container_id_label = tk.Label(self, text="Container ID:")
        self.container_id_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        self.container_id_value_label = tk.Label(self, text="")
        self.container_id_value_label.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        self.sensor_info_label = tk.Label(self, text="")
        self.sensor_info_label.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

    """def show_container_details(self, container_id):
        container = self.session.query(Container).filter_by(container_id=container_id).first()
        sensors = container.sensors

        # Get sensor readings for each sensor in the container
        sensor_data = {}
        for i, sensor in enumerate(sensors):
            sensor_data[sensor] = generate_sensor_data(container_id.plant_id.sensor_location)

        # Plot the sensor data
        plt.figure(figsize=(10, 6))
        plt.title("Sensor Readings for Container {}".format(container_id))
        for i, (sensor, data) in enumerate(sensor_data.items()):
            plt.plot(data, label="Sensor {}".format(i+1))

        plt.xlabel("Time")
        plt.ylabel("Sensor Reading")
        plt.legend()
        plt.show()

        # Update the container ID label
        self.container_id_value_label.configure(text=str(container_id))

        # Initialize the sensor information string
        sensor_info = ""

        # Loop over all sensors in the container and add their information to the sensor information string
        for sensor in Container.sensors:
            sensor_info += f"Location: {sensor.sensor_location}\n"
            if sensor.moisture is not None:
                sensor_info += f"Moisture reading: {sensor.moisture:.2f}\n"
            if sensor.light is not None:
                sensor_info += f"Light reading: {sensor.light}\n"
            sensor_info += f"Substrate recommendation: {sensor.substrate_recommendation}\n\n"

        # Update the sensor information label
         
        self.sensor_info_label.configure(text="\n".join(sensor_data.values()))"""

