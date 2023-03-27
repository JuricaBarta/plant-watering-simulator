from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import random
from datetime import datetime


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    def __init__(self, name, surname, username, password):
        self.name = name
        self.surname = surname
        self.username = username
        self.password = password

class Plant(Base):
    __tablename__ = "plants"

    plant_id = Column(Integer, primary_key=True)
    plant_name = Column(String, nullable=False)
    plant_description_one = Column(String)
    plant_description_two = Column(String)
    plant_images = relationship('PlantImage', back_populates='plant')
    containers = relationship('Container', back_populates='plant')

    def __init__(self, plant_name, plant_description_one=None, plant_description_two=None):
        self.plant_name = plant_name
        self.plant_description_one = plant_description_one
        self.plant_description_two = plant_description_two

class PlantImage(Base):
    __tablename__ = "plant_images"

    plant_image_id = Column(Integer, primary_key=True)
    plant_image_name = Column(String)
    plant_id = Column(Integer, ForeignKey('plants.plant_id'))

    plant = relationship('Plant', back_populates='plant_images')

    def __init__(self, plant_image_name, plant=None):
        self.plant_image_name = plant_image_name
        if plant is not None:
            self.plant_id = plant.plant_id
            self.plant = plant

class Container(Base):
    __tablename__ = "containers"

    container_id = Column(Integer, primary_key=True)
    container_material = Column(String)
    container_location = Column(String, nullable=False)
    plant_id = Column(Integer, ForeignKey('plants.plant_id'))
    
    plant = relationship('Plant', back_populates='containers')
    sensors = relationship('Sensor', back_populates='container')

    def __init__(self, container_material, container_location):
        self.container_location = container_location
        self.container_material = container_material

class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True)
    sensor_type = Column(String, nullable=False)
    moisture = Column(Float)
    light = Column(Float)
    soil = Column(Float)

    container_id = Column(Integer, ForeignKey('containers.container_id'))
    container = relationship('Container', back_populates='sensors')

    def __init__(self, sensor_type, container_id, moisture=None, light=None, soil=None):
        container = session.query(Container).filter_by(container_id=container_id).first()
        if container is None:
            raise ValueError(f"Container with id {container_id} does not exist in the database.")

        self.sensor_type = sensor_type
        self.container = container
        self.moisture = moisture
        self.light = light
        self.soil = soil


# Kreiranje baze podataka i dodavanje korisnika u tablicu
engine = create_engine("sqlite:///database.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

#Class User

result = session.query(User).count()
if result == 0:
    user1 = User(name="Jurica", surname="Barta", username="Jura", password="1234")
    user2 = User(name="Davor", surname="Skalec", username="Davor", password="1234")
    user3 = User(name="j", surname="j", username="j", password="j")
    
    session.add(user1)
    session.add(user2)
    session.add(user3)
   
    session.commit()
    
    print("Korisnici su uspješno uneseni u tablicu.")
    print(f"user1: Name: {user1.name} Surname: {user1.surname} Username: {user1.username} Password: {user1.password}")
    print(f"user2: Name: {user2.name} Surname: {user2.surname} Username: {user2.username} Password: {user2.password}")
    print(f"user3: Name: {user3.name} Surname: {user3.surname} Username: {user3.username} Password: {user3.password}")
else:
    print("Users have already been saved in the database.")

# Class Plant

if session.query(Plant).count() == 0:
    plant_names = ['Acer', 'Anthurium', 'Bamboo', 'Calla', 'Davallia Fejeensis',
                'Dracena Marginata', 'Epipremnum', 'Monstera Deliciosa',
                'Pillea Elefantore', 'Spatifilum']
    plant_descriptions = {
        'Acer': ('Deciduous tree', 'Known for its colorful foliage'),
        'Anthurium': ('Tropical plant', 'Produces heart-shaped flowers'),
        'Bamboo': ('Fast-growing grass', 'Used for construction and as food for animals'),
        'Calla': ('Perennial herb', 'Produces trumpet-shaped flowers'),
        'Davallia Fejeensis': ('Epiphytic fern', 'Native to Fiji'),
        'Dracena Marginata': ('Evergreen tree', 'Long, slender leaves with red edges'),
        'Epipremnum': ('Epiphytic vine', 'Often used as a houseplant'),
        'Monstera Deliciosa': ('Tropical vine', 'Produces large, perforated leaves'),
        'Pillea Elefantore': ('Herbaceous perennial', 'Also known as "Chinese money plant"'),
        'Spatifilum': ('Flowering plant', 'Produces white or pink flowers')
    }
    for plant_name in plant_names:
        plant_description = plant_descriptions[plant_name]
        plant = Plant(plant_name=plant_name,
                    plant_description_one=plant_description[0],
                    plant_description_two=plant_description[1])
        session.add(plant)
        session.commit()
else:
    print("Plants have already been saved in the database.")

# Class plantImage
if session.query(PlantImage).count() == 0:
    plant_image_names = ['acer.jpg', 'anthurium.jpg', 'bamboo.jpg', 'calla.jpg',
                         'davallia_fejeensis.jpg', 'dracena_marginata.jpg',
                         'epipremnum.jpg', 'monstera_deliciosa.jpg',
                         'pillea_elefantore.jpg', 'spatifilum.jpg']

    for i, plant_name in enumerate(plant_names):
        plant = session.query(Plant).filter_by(plant_name=plant_name).first()
        if plant is None:
            plant = Plant(plant_name=plant_name,
                          plant_description_one=plant_descriptions[plant_name][0],
                          plant_description_two=plant_descriptions[plant_name][1])
            session.add(plant)
            session.commit()

        plant_image = PlantImage(plant_image_name=plant_image_names[i], plant=plant)
        session.add(plant_image)
        session.commit()

#Class Container


# kreiranje 10 posuda samo ako ih nema u bazi
if session.query(Container).count() == 0:
    container_locations = ['Kitchen', 'Balcony', 'Living room']
    for i, plant_name in enumerate(plant_names):
        plant = session.query(Plant).filter_by(plant_name=plant_name).first()
        container = session.query(Container).filter_by(container_location=container_locations[i % len(container_locations)]).first()
        if container is None and plant is not None:
            container = Container(container_material='material', container_location=container_locations[i % len(container_locations)])
            container.plant = plant
            session.add(container)
            session.commit()
else:
    print("Containers have already been saved in the database.")


# Class Sensor

# create sensors for the newly created containers
if session.query(Sensor).count() == 0:
    for sensor_type in ['moisture', 'light', 'soil']:
        sensor_location = container_locations
        moisture = random.uniform(0, 100) if sensor_type == 'moisture' else None
        light = random.uniform(0, 2000) if sensor_type == 'light' else None
        soil = random.uniform(0, 10) if sensor_type == 'soil' else None

        sensor = Sensor(sensor_type=sensor_type,
                container_id=container.container_id,
                moisture=moisture,
                light=light,
                soil=soil)

        session.add(sensor)
        session.commit()
else:
    print("Sensors have already been saved in the database.")
