import tkinter as tk
from tkinter import ttk, Label
from crud import *
from database import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ContainerDetails(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.plant_image_label = Label(self, image=None)
        self.plant_image_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.label = tk.LabelFrame(self, text="Container Details")
        self.label.grid(row=1, column=0, padx=10, pady=10)

        self.plant_picture = tk.Label(self.label)
        self.plant_picture.grid(row=0, column=0, padx=10, pady=10)

        self.plant_name_label = tk.Label(self.label, text="")
        self.plant_name_label.grid(row=1, column=0, padx=10, pady=10)

        self.plant_description_label = tk.Label(self.label, text="", anchor="w")
        self.plant_description_label.grid(row=2, column=0, padx=10, pady=10)

        button_previous_plant = tk.Button(self, text="Previous Plant", command=self.previous_plant)
        button_previous_plant.grid(row=3, column=0, padx=10, pady=10, sticky="w")  

        button_next_plant = tk.Button(self, text="Next Plant", command=self.next_plant)
        button_next_plant.grid(row=3, column=1, padx=10, pady=10, sticky="e")

        self.plants = session.query(Plant).all()
        self.current_plant_index = 0

    def next_plant(self):
        # go to the next plant and display it
        if self.current_plant_index < len(self.plants) - 1:
            self.current_plant_index += 1
            container_name = self.plants[self.current_plant_index].plant_name
            try:
                container_index = self.master.children['!containersscreen'].plant_names.index(container_name)
            except ValueError:
                print("There are no more containers in the database.")
                return
            self.update_container_data(container_name)

    def previous_plant(self):
        # go to the previous plant and display it
        if self.current_plant_index > 0:
            self.current_plant_index -= 1
            container_name = self.plants[self.current_plant_index].plant_name
            try:
                container_index = self.master.children['!containersscreen'].plant_names.index(container_name)
            except ValueError:
                print("There are no more containers in the database.")
                return
            self.update_container_data(container_name)


    def update_container_image(self, container_image):
        # Update the container image
        plant_image = Image.open(container_image)
        plant_image = plant_image.resize((250, 250), Image.ANTIALIAS)
        plant_image_tk = ImageTk.PhotoImage(plant_image)
        self.plant_image_label.configure(image=plant_image_tk)
        self.plant_image_label.image = plant_image_tk


    def generate_sensor_data(self, sensor_type, sync=False):
        # Generate random sensor data
        if not sync:
            if sensor_type == "Moisture":
                moisture = random.uniform(0, 100)
                if moisture <= 40:
                    message = "The soil is dry. You should water the plant."
                elif moisture <= 60:
                    message = "The plant has enough water."
                else:
                    message = "The plant has too much water. Check the bottom of the pot and remove excess water."
                return message, moisture
            elif sensor_type == "Light":
                light = random.uniform(0, 10000)
                if light <= 4000:
                    message = "The plant has too little light. It would be good to move it to a brighter location."
                elif light <= 6000:
                    message = "The plant has enough light during the day. No changes are necessary."
                else:
                    message = "The plant has too much light. It would be good to move it to a darker area."
                return message, light
            elif sensor_type == "Soil":
                soil = random.uniform(0, 14)
                if soil < 5.5:
                    message = "The soil is too acidic. You should add lime."
                elif soil <= 7.5:
                    message = "The soil pH value is good."
                else:
                    message = "The soil is too alkaline. You should add fertilizer."
                return message, soil
        else:
            if sensor_type == "Moisture":
                return "The soil has enough water", 40.00
            elif sensor_type == "Light":
                return "The plant has enough light during the day", 5000.00
            elif sensor_type == "Soil":
                return "The soil pH value is good", 7.00
        
           
    def update_sensor_labels(self, container_sensors):
        # Update the sensor labels
        sensor_values = [sensor_label.cget("text") for sensor_label in container_sensors]
        sensor_text = "\n".join([f"{sensor_type}: {sensor_value}" for sensor_type, sensor_value in zip(["Moisture", "Light", "Soil"], sensor_values)])
        self.plant_description_label.configure(text=sensor_text)

    def update_container_data(self, container_name):
        # Find the container data in the ContainersScreen
        container_index = self.master.children['!containersscreen'].plant_names.index(container_name)
        container_image = self.master.children['!containersscreen'].plant_images[container_index]
        container_sensors = self.master.children['!containersscreen'].sensor_labels[container_index * 3: (container_index + 1) * 3]

        # Update the container image and sensor labels
        self.update_container_image(container_image)
        self.update_sensor_labels(container_sensors)

         # Gumb za promjenu vrste grafa
        self.graph_type = 1
        self.graph_button = tk.Button(self, text="Change Graph Type", command=self.change_graph_type)
        self.graph_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        self.plants = session.query(Plant).all()
        self.current_plant_index = 0

    def change_graph_type(self):
        # Promjena vrste grafa
        self.graph_type = (self.graph_type % 3) + 1
        self.generate_graph()

    def generate_graph(self):
        # Create a canvas to display the graphs in the tkinter application
        canvas = FigureCanvasTkAgg(plt.Figure(), master=self)
        canvas.get_tk_widget().grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Get the moisture, light, and soil data from the current tab
        tab2 = self.master.nametowidget(self.master.select())

        # Create a subplot for all three sensors
        fig, ax = plt.subplots(figsize=(12, 6))

        # Set colors for each sensor type
        colors = {"Moisture": "blue", "Light": "yellow", "Soil": "brown"}

        if self.graph_type == 1:
            # Line chart
            for sensor_type in colors:
                readings = []
                for i in range(5):
                    message, value = tab2.generate_sensor_data(sensor_type, sync=False)
                    readings.append(value)
                normalized_readings = normalize_sensor_data(readings)
                ax.plot([1, 2, 3, 4, 5], normalized_readings, label=sensor_type, color=colors[sensor_type])
            ax.set_title("Line Chart")
            ax.set_xlabel("X Label")
            ax.set_ylabel("Y Label")
            ax.legend()

        elif self.graph_type == 2:
            # Pie chart
            values = []
            labels = []
            for sensor_type in colors:
                message, value = tab2.generate_sensor_data(sensor_type, sync=False)
                values.append(value)
                labels.append(sensor_type)
            ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
            ax.set_title("Pie Chart")

        elif self.graph_type == 3:
            # Histogram
            for sensor_type in colors:
                readings = []
                for i in range(5):
                    message, value = tab2.generate_sensor_data(sensor_type, sync=False)
                    readings.append(value)
                ax.hist(readings, bins=5, label=sensor_type, color=colors[sensor_type], alpha=0.5)
            ax.set_title("Histogram")
            ax.set_xlabel("Value")
            ax.set_ylabel("Frequency")
            ax.legend()

        # Draw the canvas
        canvas.figure = fig
        canvas.draw()

def normalize_sensor_data(sensor_data):
        min_value = min(sensor_data)
        max_value = max(sensor_data)
        if min_value == max_value:
            return [50] * len(sensor_data)  # Handle the case where all values are the same
        normalized_data = [(value - min_value) / (max_value - min_value) * 100 for value in sensor_data]
        return normalized_data