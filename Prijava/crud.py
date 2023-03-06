from PIL import Image, ImageTk
import tkinter as tk
from database import session, Plant, Container, Sensor
import random
from datetime import datetime
from sqlalchemy.orm import Session
#from biljke.kreiranje_nove_biljke import *

class PlantImage:
    def __init__(self, filename, size=(150, 200)):
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

def read_sensors(plant_id, moisture_level, light, temperature, substrate, recommended_watering_frequency, recommended_light_exposure, recommended_substrate_amendment):
    sensor = Sensor(
        plant_id, 
        moisture_level, 
        light, 
        temperature, 
        substrate, 
        recommended_watering_frequency=recommended_watering_frequency, 
        recommended_light_exposure=recommended_light_exposure, 
        recommended_substrate_amendment=recommended_substrate_amendment
        )

def generate_readings(self):
        if self.sensor_type == "moisture":
            return random.uniform(0.0, 100.0)
        elif self.sensor_type == "light":
            return random.uniform(0.0, 2000.0)
        elif self.sensor_type == "substrate":
            return random.choice(["add compost", "add vermiculite", "add perlite"])
        else:
            raise ValueError(f"Invalid sensor type: {self.sensor_type}")

def generate_sensor_readings(session):
    sensors = session.query(Sensor).all()
    for sensor in sensors:
        if sensor.sensor_type in ["moisture", "light", "substrate"]:
            reading = sensor.generate_readings()
            if sensor.sensor_type == "moisture":
                sensor.moisture = reading
            elif sensor.sensor_type == "light":
                sensor.light = reading
            elif sensor.sensor_type == "substrate":
                sensor.substrate_recommendation = reading
            session.add(sensor)
    session.commit()
