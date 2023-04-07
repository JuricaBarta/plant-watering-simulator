import tkinter as tk
from tkinter import ttk
from crud import *
from database import *

class ContainerDetails(tk.Frame):
    def __init__(self, parent, container_name):
        super().__init__(parent)
        self.container_name = container_name

        self.label = ttk.LabelFrame(self, text=f"Details for container {container_name}")
        self.label.grid(padx=10, pady=10)

        # Add labels to display data from container 1 in tab 2
        label1 = tk.Label(self.label, text=f"Container name: {container_name}")
        label1.pack(pady=5)

        label2 = tk.Label(self.label, text="Sensor data:")
        label2.pack(pady=5)

        # Create a frame to contain the sensor data labels
        sensor_frame = tk.Frame(self.label)
        sensor_frame.pack(side=tk.TOP)

    def set_container_name(self, container_name):
        self.container_name = container_name

        """# Create labels to display the sensor data
        moisture_label = tk.Label(sensor_type, text=self.generate_sensor_data(sensor_type))
        moisture_label.pack(side=tk.TOP, padx=5, pady=5)
        
        light_label = tk.Label(sensor_type, text=self.generate_sensor_data(sensor_type))
        light_label.pack(side=tk.TOP, padx=5, pady=5)
        
        soil_label = tk.Label(sensor_type, text=self.generate_sensor_data(sensor_type))
        soil_label.pack(side=tk.TOP, padx=5, pady=5)

        # Add a button to switch back to tab 1
        button = tk.Button(self.label, text="Go back to Containers", command=self.switch_to_tab1)
        button.pack(pady=10)"""

    def generate_sensor_data(self, sensor_type, ideal=False):
        if not ideal:
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

    def switch_to_tab1(self):
        self.master.switch_frame("ContainersScreen")
