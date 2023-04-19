from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import random
from datetime import datetime
import os


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

    plant_id = Column(Integer, primary_key=True, autoincrement=True)
    plant_name = Column(String, nullable=False)
    plant_description_one = Column(String)
    plant_description_two = Column(String)
    plant_description_three = Column(String)
    plant_description_four = Column(String)
    
    plant_images = relationship('PlantImage', back_populates='plant')
    containers = relationship('Container', back_populates='plant')

    def __init__(self, plant_name, plant_description_one=None, plant_description_two=None, plant_description_three=None, plant_description_four=None):
        self.plant_name = plant_name
        self.plant_description_one = plant_description_one
        self.plant_description_two = plant_description_two
        self.plant_description_three = plant_description_three
        self.plant_description_four = plant_description_four


class PlantImage(Base):
    __tablename__ = 'plant_image'

    id = Column(Integer, primary_key=True)
    plant_image_name = Column(String(100), nullable=False)
    plant_id = Column(Integer, ForeignKey('plants.plant_id'), nullable=False)
    image_path = Column(String(200), nullable=False)

    plant = relationship('Plant', back_populates='plant_images')

    def __repr__(self):
        return f"<PlantImage {self.plant_image_name}>"

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
        if moisture is not None:
            self.moisture = moisture
        if light is not None:
            self.light = light
        if soil is not None:
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
    plant_names = ["Acer", "Anthurium", "Bamboo", "Calla", "Davallia Fejeensis",
                "Dracena Marginata", "Epipremnum", "Monstera Deliciosa",
                "Pillea Elefantore", "Spatifilum"]
                
    plant_descriptions = {
        "Acer": ("Deciduous tree", "Known for its colorful foliage", "Provides a source of maple syrup when tapped during the spring", "Has a wide range of cultivars, including those with unique leaf shapes such as the Japanese maple"),
        "Anthurium": ("Tropical plant", "Produces heart-shaped flowers", "Has a long blooming period, with flowers lasting up to 8 weeks", "Comes in a variety of colors including pink, red, white, and orange"),
        "Bamboo": ("Fast-growing grass", "Used for construction and as food for animals", "Contains anti-bacterial and anti-inflammatory properties", "Can absorb up to 12 tons of carbon dioxide per hectare, making it an effective tool against climate change"),
        "Calla": ("Perennial herb", "Produces trumpet-shaped flowers", "Symbolizes rebirth and resurrection", "Has medicinal uses, such as treatment for swelling and skin irritation"),
        "Davallia Fejeensis": ("Epiphytic fern", "Native to Fiji", "Also known as the rabbit's foot fern due to its furry rhizomes", "Thrives in low-light environments and is easy to care for"),
        "Dracena Marginata": ("Evergreen tree", "Long, slender leaves with red edges", "Can grow up to 15 feet tall in optimal conditions", "Air-purifying and removes toxins such as benzene, formaldehyde, and trichloroethylene from the air"),
        "Epipremnum": ("Epiphytic vine", "Often used as a houseplant", "Can improve indoor air quality by removing pollutants such as formaldehyde, benzene, and xylene", "Has a unique variegated leaf pattern, with shades of green, white, and yellow"),
        "Monstera Deliciosa": ("Tropical vine", "Produces large, perforated leaves", "Symbolizes the pursuit of knowledge and a thirst for exploration", "Thrives in high humidity environments and is known for its adaptability to various light conditions"),
        "Pillea Elefantore": ("Herbaceous perennial", 'Also known as "Chinese money plant"', "Symbolizes financial prosperity and good luck", "Thrives in well-draining soil and bright, indirect light"),
        "Spatifilum": ("Flowering plant", "Produces white or pink flowers", "Symbolizes peace and tranquility", "Air-purifying and removes toxins such as benzene, formaldehyde, and trichloroethylene from the air")
    }

    for plant_name in plant_names:
        plant_description = plant_descriptions[plant_name]
        plant = Plant(plant_name=plant_name,
                    plant_description_one=plant_description[0],
                    plant_description_two=plant_description[1],
                    plant_description_three=plant_description[2],
                    plant_description_four=plant_description[3])
        session.add(plant)
        session.commit()
else:
    print("Plants have already been saved in the database.")


plant_image_names = ['acer.jpg', 'anthurium.jpg', 'bamboo.jpg', 'calla.jpg',
                     'davallia_fejeensis.jpg', 'dracena_marginata.jpg',
                     'epipremnum.jpg', 'monstera_deliciosa.jpg',
                     'pillea_elefantore.jpg', 'spatifilum.jpg']

if session.query(PlantImage).count() == 0:
    # Directory containing the plant images
    plant_images_dir = os.path.dirname(os.path.abspath(__file__))

    # Get a list of unique plant names
    plant_names = [plant.plant_name for plant in session.query(Plant.plant_name).distinct()]

    for i, plant_name in enumerate(plant_names):
        plant = session.query(Plant).filter_by(plant_name=plant_name).first()

        # Create the image path based on the plant image name and the directory containing the images
        image_path = os.path.join(plant_images_dir, plant_image_names[i])

        # Create a new PlantImage instance and add it to the session
        plant_image = PlantImage(plant_image_name=plant_image_names[i],
                                 plant=plant,
                                 image_path=image_path) 
        session.add(plant_image)
        session.commit()
else:
    print("Plant images have already been saved in the database.")


#Class Container
# kreiranje 3 posuda samo ako ih nema u bazi
if session.query(Container).count() == 0:
    container_locations = ['Kitchen', 'Balcony', 'Living room']
    for i, plant_name in enumerate(plant_names):
        for j in range(1):
            container = session.query(Container).filter_by(container_location=f"{container_locations[i % len(container_locations)]}-{j}").first()
            if container is None and plant is not None:
                container = Container(container_material='material', container_location=f"{container_locations[i % len(container_locations)]}-{j}")
                container.plant = plant
                session.add(container)
                session.commit()
else:
    print("Containers have already been saved in the database.")


# Class Sensor

# create sensors for the newly created containers
if session.query(Sensor).count() == 0:
    for sensor_type in ['moisture', 'light', 'soil']:
        for container_location in container_locations:
            for j in range(1):
                container = session.query(Container).filter_by(container_location=f"{container_location}-{j}").first()
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

