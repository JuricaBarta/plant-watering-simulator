from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from database import *
from PIL import Image, ImageTk
import random

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
    

def sync_sensors(container_id):
    container = session.query(Container).get(container_id)
    if container is None:
        raise ValueError(f"Container with id {container_id} does not exist in the database.")
    sensor_type = (['Moisture', 'Light', 'Soil'])
    moisture = int(50)
    light = int(5000)
    soil = int(7)
    return create_sensor(sensor_type, container_id, moisture, light, soil)


# CREATE
def create_user(name, surname, username, password):
    user = User(name=name, surname=surname, username=username, password=password)
    session.add(user)
    session.commit()
    return user

def create_plant(plant_name, plant_description_one=None, plant_description_two=None):
    plant = Plant(plant_name=plant_name, plant_description_one=plant_description_one,
                  plant_description_two=plant_description_two)
    session.add(plant)
    session.commit()
    return plant

def create_plant_image(plant_image_name, plant_id):
    plant = session.query(Plant).get(plant_id)
    if plant is None:
        raise ValueError(f"Plant with id {plant_id} does not exist in the database.")
    plant_image = PlantImage(plant_image_name=plant_image_name, plant=plant)
    session.add(plant_image)
    session.commit()
    return plant_image

def create_container(container_material, container_location, plant_id):
    plant = session.query(Plant).get(plant_id)
    if plant is None:
        raise ValueError(f"Plant with id {plant_id} does not exist in the database.")
    container = Container(container_material=container_material, container_location=container_location, plant=plant)
    session.add(container)
    session.commit()
    return container

def create_sensor(sensor_type, container_id, moisture=None, light=None, soil=None):
    container = session.query(Container).get(container_id)
    if container is None:
        raise ValueError(f"Container with id {container_id} does not exist in the database.")
    sensor = Sensor(sensor_type=sensor_type, container=container, moisture=moisture, light=light, soil=soil)
    session.add(sensor)
    session.commit()
    return sensor

# READ
def get_user_by_id(user_id):
    return session.query(User).get(user_id)

def get_user_by_username(username):
    return session.query(User).filter_by(username=username).first()

def get_all_plants():
    return session.query(Plant).all()

def get_plant_by_id(plant_id):
    return session.query(Plant).get(plant_id)

def get_plant_images_by_plant_id(plant_id):
    if isinstance(plant_id, list):
        return session.query(PlantImage).filter(*[PlantImage.plant_id == p for p in plant_id]).all()
    else:
        return session.query(PlantImage).filter_by(plant_id=plant_id).all()

def get_containers_by_plant_id(plant_id):
    return session.query(Container).filter_by(plant_id=plant_id).all()

def get_container_by_name(container_name):
    return session.query(Container).filter_by(container_location=container_name).first()


def get_sensor_by_id(sensor_id):
    return session.query(Sensor).get(sensor_id)


# UPDATE
def update_user(user_id, name=None, surname=None, username=None, password=None):
    user = session.query(User).get(user_id)
    if user is None:
        raise ValueError(f"User with id {user_id} does not exist in the database.")
    if name is not None:
        user.name = name
    if surname is not None:
        user.surname = surname
    if username is not None:
        user.username = username
    if password is not None:
        user.password = password
    session.commit()
    return user

def update_plant(plant_id, plant_name=None, plant_description_one=None, plant_description_two=None):
    plant = session.query(Plant).get(plant_id)
    if plant is None:
        raise ValueError(f"Plant with id {plant_id} does not exist in the database.")
    if plant_name is not None:
        plant.plant_name = plant_name
    if plant_description_one is not None:
        plant.plant_description_one = plant_description_one
    if plant_description_two is not None:
        plant.plant_description_two = plant_description_two
    session.commit()
    return plant

def update_plant_image(plant_image_id, plant_image_name=None, plant_id=None):
    plant_image = session.query(PlantImage).get(plant_image_id)
    if plant_image is None:
        raise ValueError(f"Plant image with id {plant_image_id} does not exist in the database.")
    if plant_image_name is not None:
        plant_image.plant_image_name = plant_image_name
    if plant_id is not None:
        plant = session.query(Plant).get(plant_id)
        if plant is None:
            raise ValueError(f"Plant with id {plant_id} does not exist in the database.")
        plant_image.plant = plant
    session.commit()
    return plant_image

def update_container(container_id, container_material=None, container_location=None, plant_id=None):
    container = session.query(Container).get(container_id)
    if container is None:
        raise ValueError(f"Container with id {container_id} does not exist in the database.")
    if container_material is not None:
        container.container_material = container_material
    if container_location is not None:
        container.container_location = container_location
    if plant_id is not None:
        plant = session.query(Plant).get(plant_id)
        if plant is None:
            raise ValueError(f"Plant with id {plant_id} does not exist in the database.")
        container.plant = plant
    session.commit()
    return container

def update_sensor(sensor_id, sensor_type=None, container_id=None, moisture=None, light=None, soil=None):
    sensor = session.query(Sensor).get(sensor_id)
    if sensor is None:
        raise ValueError(f"Sensor with id {sensor_id} does not exist in the database.")
    if sensor_type is not None:
        sensor.sensor_type = sensor_type
    if container_id is not None:
        container = session.query(Container).get(container_id)
        if container is None:
            raise ValueError(f"Container with id {container_id} does not exist in the database.")
        sensor.container = container
    if moisture is not None:
        sensor.moisture = moisture
    if light is not None:
        sensor.light = light
    if soil is not None:
        sensor.soil = soil
    session.commit()
    return sensor

# DELETE

def delete_user(session: Session, user_id: int):
    user = session.query(User).get(user_id)
    if user is None:
        raise ValueError(f"User with id {user_id} does not exist in the database.")
    session.delete(user)
    session.commit()

def delete_plant(session, plant_id):
    session.query(PlantImage).filter(PlantImage.plant_id == plant_id).delete()
    session.query(Plant).filter_by(plant_id=plant_id).delete()
    session.commit()

def delete_plant_image(session: Session, plant_image_id: int):
    plant_image = session.query(PlantImage).get(plant_image_id)
    if plant_image is None:
        raise ValueError(f"Plant image with id {plant_image_id} does not exist in the database.")
    session.delete(plant_image)
    session.commit()

def delete_container(session: Session, container_id: int):
    container = session.query(Container).get(container_id)
    if container is None:
        raise ValueError(f"Container with id {container_id} does not exist in the database.")
    session.delete(container)
    session.commit()

def delete_sensor(session: Session, sensor_id: int):
    sensor = session.query(Sensor).get(sensor_id)
    if sensor is None:
        raise ValueError(f"Sensor with id {sensor_id} does not exist in the database.")
    session.delete(sensor)
    session.commit()

# GENERATE DATA

def generate_sensor_data(sensor_type):
    if sensor_type == "moisture":
        return random.uniform(0.0, 100.0)
    elif sensor_type == "light":
        return random.uniform(0.0, 2000.0)
    elif sensor_type == "substrate":
        return random.choice(["add compost", "add vermiculite", "add perlite"])
    else:
        raise ValueError(f"Invalid sensor type: {sensor_type}")

def generate_user():
    name = name()
    surname = surname()
    username = username()
    password = password()
    return create_user(name, surname, username, password)

def generate_plant():
    plant_name = plant_name()
    plant_description_one = plant_name()
    plant_description_two = plant_name()
    plant_description_three = plant_name()
    plant_description_four = plant_name()
    return create_plant(plant_name, plant_description_one, plant_description_two, plant_description_three, plant_description_four)

def generate_plant_image(plant_id):
    plant = session.query(Plant).get(plant_id)
    if plant is None:
        raise ValueError(f"Plant with id {plant_id} does not exist in the database.")
    plant_image_name = plant_image_name()
    return create_plant_image(plant_image_name, plant_id)

def generate_container(plant_id):
    plant = session.query(Plant).get(plant_id)
    if plant is None:
        raise ValueError(f"Plant with id {plant_id} does not exist in the database.")
    container_material = container_material()
    container_location = container_location()
    return create_container(container_material, container_location, plant_id)

def generate_sensor(container_id):
    container = session.query(Container).get(container_id)
    if container is None:
        raise ValueError(f"Container with id {container_id} does not exist in the database.")
    sensor_type = random.choice(['Moisture', 'Light', 'Soil'])
    moisture = random.randint(0, 100)
    light = random.randint(0, 100)
    soil = random.randint(0, 100)
    return create_sensor(sensor_type, container_id, moisture, light, soil)


"""# HELPER FUNCTIONS

def generate_name():
    letters = string.ascii_lowercase
    name_length = random.randint(4, 10)
    return ''.join(random.choice(letters) for i in range(name_length)).capitalize()

def generate_username():
    letters = string.ascii_lowercase
    username_length = random.randint(8, 12)
    return ''.join(random.choice(letters) for i in range(username_length))

def generate_password():
    letters = string.ascii_letters + string.digits + string.punctuation
    password_length = random.randint(8, 12)
    return ''.join(random.choice(letters) for i in range(password_length))

def generate_word():
    letters = string.ascii_lowercase
    word_length = random.randint(4, 10)
    return ''.join(random.choice(letters) for i in range(word_length))

def generate_sentence():
    words = [generate_word() for i in range(5)]
    sentence = ' '.join(words)
    return sentence.capitalize() + '.'"""
