from PIL import Image, ImageTk
import tkinter as tk
from database import session, Plant, Container, Sensor
import random
from datetime import datetime
from sqlalchemy.orm import Session
from typing import List
#from biljke.kreiranje_nove_biljke import *

def create_image(self, filename, size=(150, 200)):
    self.filename = filename
    self.size = size
    self.photo = self.open_and_resize() 
    
def open_and_resize(self):
    picture = Image.open(self.filename)
    resized = picture.resize(self.size, Image.LANCZOS)
    return ImageTk.PhotoImage(resized)

def get_image(self):
    self.photo.image = self.photo
    return self.photo



def create_plant(plant_name, plant_image=None):
    plant = Plant(plant_name=plant_name, plant_image=plant_image)
    session.add(plant)
    session.commit()

def update_plant(plant_id, plant_name=None, plant_image=None):
    plant = session.query(Plant).get(plant_id)

    if plant_name is not None:
        plant.plant_name = plant_name
    if plant_image is not None:
        plant.plant_image = plant_image

    session.commit()

def delete_plant(plant_id):
    plant = session.query(Plant).get(plant_id)
    session.delete(plant)
    session.commit()


def create_container(location, plant_id):
    container = Container(location=location, plant_id=plant_id)
    session.add(container)
    session.commit()

def delete_container(container_id):
    container = session.query(Container).filter_by(id=container_id).one()
    session.delete(container)
    session.commit()

def generate_sensor_data(plant_name, container):
    session = Session()

    # Get the container associated with the specified plant
def generate_sensor_data(plant_name, container):
    session = Session()

    # Get the container associated with the specified plant
    container = session.query(Container).join(Container.plant).filter(Plant.plant_name == plant_name).first()

    sensor_info = ''
    if container:
        for sensor in container.sensors:
            if sensor.sensor_type == 'substrate':
                if random.random() < 0.5:
                    sensor.substrate_recommendation = "Add fertilizer"
                else:
                    sensor.substrate_recommendation = "None"
            elif sensor.sensor_type == 'moisture':
                sensor.moisture = random.uniform(0, 100)
                if sensor.moisture < 50:
                    sensor_info += "Plant needs more water\n"
                elif sensor.moisture > 75:
                    sensor_info += "Plant has too much water\n"
                else:
                    sensor_info += f"Plant has {sensor.moisture}% of water\n"
            elif sensor.sensor_type == 'light':
                sensor.light = random.uniform(0, 2000)
                if sensor.light < 1000:
                    sensor_info += "Plant needs more light\n"
                elif sensor.light > 2000:
                    sensor_info += "Plant has too much light\n"
                else:
                    sensor_info += f"Plant has {sensor.light} lumens per watt of light\n"
            elif sensor.sensor_type == 'temperature':
                sensor.temperature = random.uniform(10, 40)
                if sensor.temperature < 20:
                    sensor_info += "Plant is too cold\n"
                elif sensor.temperature > 30:
                    sensor_info += "Plant is too hot\n"


        session.commit()
        session.close()

        return sensor_info
    else:
        session.close()
        return f"No container found for plant {plant_name}"

