from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError
import random
import os


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
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
    plant_description = Column(String)  # Combining description one and two
    moisture_info = Column(String)  # Recommendation for moisture (e.g., 'daily', 'weekly', 'monthly')
    light_temp_info = Column(String)  # Recommendation for light and temperature (e.g., 'bright, warm', 'low, cool')
    substrates = Column(String)  # Recommendation for substrates

    image_path = Column(String)

    plant_images = relationship('PlantImage', back_populates='plant', cascade="all, delete-orphan")
    containers = relationship('Container', back_populates='plant')

    def __init__(self, plant_name, plant_description=None, moisture_info=None, light_temp_info=None, substrates=None):
        self.plant_name = plant_name
        self.plant_description = plant_description
        self.moisture_info = moisture_info
        self.light_temp_info = light_temp_info
        self.substrates = substrates



class PlantImage(Base):
    __tablename__ = 'plant_image'

    id = Column(Integer, primary_key=True, index=True)
    plant_image_name = Column(String(100), nullable=False)
    image_path = Column(String(200), nullable=False)
    plant_id = Column(Integer, ForeignKey('plants.plant_id'), nullable=False)

    plant = relationship('Plant', back_populates='plant_images')

    def __repr__(self):
        return f"<PlantImage {self.plant_image_name}>"


class Container(Base):
    __tablename__ = "containers"

    container_id = Column(Integer, primary_key=True, autoincrement=True)
    container_material = Column(String)
    container_location = Column(String, nullable=False)
    plant_id = Column(Integer, ForeignKey('plants.plant_id'))

    plant = relationship('Plant', back_populates='containers')
    sensors = relationship('Sensor', back_populates='container')

    def __init__(self, container_material, container_location, plant_id):
        self.container_location = container_location
        self.container_material = container_material
        self.plant_id = plant_id


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

def add_user(name, surname, username, password):
    new_user = User(name=name, surname=surname, username=username, password=password)

    try:
        session.add(new_user)
        session.commit()
        print(f"Name: '{name}', surname: '{surname}', username: '{username}', password: '{password}' successfully added.")
    except IntegrityError:
        session.rollback()
        print("Error: Username already exists. Please choose a different username.")

add_user(name="Jurica", surname="Barta", username="Jura", password="1234")
add_user(name="Davor", surname="Skalec", username="Davor", password="1234")

# Class Plant

if session.query(Plant).count() == 0:
    plants_data = {
        "Acer": {
            "plant_name": "Acer",
            "plant_description": "Acer is a deciduous tree known for its colorful foliage. \nIt provides a source of maple syrup when tapped during the spring. \nAcer has a wide range of cultivars, \nincluding those with unique leaf shapes, \nsuch as the Japanese maple.",
            "moisture_info": "Acer requires consistent moisture to thrive.",
            "light_temp_info": "It prefers bright and warm conditions.",
            "substrates": "Well-draining soil is recommended for Acer."
        },
        "Anthurium": {
            "plant_name": "Anthurium",
            "plant_description": "Anthurium is a tropical plant that produces heart-shaped flowers. It has a long blooming period, \nwith flowers lasting up to 8 weeks. \nAnthurium comes in a variety of colors, including pink, red, white, and orange.",
            "moisture_info": "Keep the soil consistently moist for Anthurium.",
            "light_temp_info": "Provide bright and warm conditions.",
            "substrates": "Use a well-draining potting mix for Anthurium."
        },
        "Bamboo": {
            "plant_name": "Bamboo",
            "plant_description": "Bamboo is a fast-growing grass used for construction and as food for animals. \nIt contains anti-bacterial and anti-inflammatory properties and \ncan absorb up to 12 tons of carbon dioxide per hectare, making it an effective tool against climate change.",
            "moisture_info": "Bamboo prefers consistently moist soil.",
            "light_temp_info": "It thrives in bright and warm conditions.",
            "substrates": "Bamboo does well in well-draining soil."
        },
        "Calla": {
            "plant_name": "Calla",
            "plant_description": "Calla is a perennial herb that produces trumpet-shaped flowers. \nIt symbolizes rebirth and resurrection and has medicinal uses, \nsuch as treatment for swelling and skin irritation.",
            "moisture_info": "Keep the soil consistently moist for Calla.",
            "light_temp_info": "Provide bright and warm conditions.",
            "substrates": "Well-draining soil is recommended for Calla."
        },
        "Davallia Fejeensis": {
            "plant_name": "Davallia Fejeensis",
            "plant_description": "Davallia Fejeensis is an epiphytic fern native to Fiji. \nIt is also known as the rabbit's foot fern due to its furry rhizomes. \nIt thrives in low-light environments and is easy to care for.",
            "moisture_info": "Keep the soil slightly moist for Davallia Fejeensis.",
            "light_temp_info": "It prefers low-light conditions.",
            "substrates": "Well-draining soil is suitable for this fern."
        },
        "Dracena Marginata": {
            "plant_name": "Dracena Marginata",
            "plant_description": "Dracena Marginata is an evergreen tree with long, slender leaves with red edges. \nIt can grow up to 15 feet tall in optimal conditions and is air-purifying, removing toxins such as \nbenzene, formaldehyde, and trichloroethylene from the air.",
            "moisture_info": "Allow the soil to dry between waterings for Dracena Marginata.",
            "light_temp_info": "It prefers bright and warm conditions.",
            "substrates": "Use well-draining soil for this plant."
        },
        "Epipremnum": {
            "plant_name": "Epipremnum",
            "plant_description": "Epipremnum is an epiphytic vine often used as a houseplant. \nIt can improve indoor air quality by removing pollutants such as formaldehyde, benzene, and xylene. \nIt has a unique variegated leaf pattern with shades of green, white, and yellow.",
            "moisture_info": "Keep the soil consistently moist for Epipremnum.",
            "light_temp_info": "It does well in bright and warm conditions.",
            "substrates": "Use a well-draining potting mix for Epipremnum."
        },
        "Monstera Deliciosa": {
            "plant_name": "Monstera Deliciosa",
            "plant_description": "Monstera Deliciosa is a tropical vine that produces large, perforated leaves. \nIt symbolizes the pursuit of knowledge and a thirst for exploration. \nIt thrives in high humidity environments and is known for its adaptability to various light conditions.",
            "moisture_info": "Keep the soil slightly moist for Monstera Deliciosa.",
            "light_temp_info": "It can tolerate a range of light conditions, from bright to low light.",
            "substrates": "Well-draining soil is suitable for Monstera Deliciosa."
        },
        "Pillea Elefantore": {
            "plant_name": "Pillea Elefantore",
            "plant_description": "Pillea Elefantore is a herbaceous perennial also known as the 'Chinese money plant.' \nIt symbolizes financial prosperity and good luck. \nIt thrives in well-draining soil and bright, indirect light.",
            "moisture_info": "Allow the soil to partially dry between waterings for Pillea Elefantore.",
            "light_temp_info": "It prefers bright, indirect light and moderate room temperatures.",
            "substrates": "Use a well-draining potting mix for this plant."
        },
        "Spatifilum": {
            "plant_name": "Spatifilum",
            "plant_description": "Spatifilum is a flowering plant that produces white or pink flowers. \nIt symbolizes peace and tranquility and is air-purifying, removing toxins such as \nbenzene, formaldehyde, and trichloroethylene from the air.",
            "moisture_info": "Keep the soil consistently moist for Spatifilum.",
            "light_temp_info": "It does well in low to moderate light conditions and prefers warmer temperatures.",
            "substrates": "Use well-draining soil for Spatifilum."
        }
    }



    for plant_name, data in plants_data.items():
        plant = Plant(plant_name=plant_name,
                    plant_description=data["plant_description"],
                    moisture_info=data["moisture_info"],
                    light_temp_info=data["light_temp_info"],
                    substrates=data["substrates"])
        session.add(plant)
        session.commit()
else:
    print("Plants have already been saved in the database.")



plant_image_names = ['acer.jpg', 'anthurium.jpg', 'bamboo.jpg', 'calla.jpg',
                     'davallia_fejeensis.jpg', 'dracena_marginata.jpg',
                     'epipremnum.jpg', 'monstera_deliciosa.jpg',
                     'pillea_elefantore.jpg', 'spatifilum.jpg']

if session.query(PlantImage).count() == 0:
    # Get a list of unique plant names
    plant_names = [plant.plant_name for plant in session.query(Plant.plant_name).distinct()]

    for i, plant_name in enumerate(plant_names):
        plant = session.query(Plant).filter_by(plant_name=plant_name).first()

        # Create the image path based on the plant image name (assuming images are in the project root directory)
        image_path = plant_image_names[i]

        # Create a new PlantImage instance and add it to the session
        plant_image = PlantImage(plant_image_name=plant_image_names[i],
                                 plant=plant,
                                 image_path=image_path) 
        session.add(plant_image)
        session.commit()
else:
    print("Plant images have already been saved in the database.")




# kreiranje 3 posuda samo ako ih nema u bazi
if session.query(Container).count() == 0:
    container_locations = ['Kitchen', 'Balcony', 'Living room']
    container_materials = ["Plastic", "Rock", "Ceramic"]
    plants = session.query(Plant).all()
    for i, plant in enumerate(plants):
        for j in range(1):
            container_location = f"{container_locations[i % len(container_locations)]}-{j}"
            container = session.query(Container).filter_by(container_location=container_location).first()
            if container is None and plant is not None:
                container_material = f"{container_materials[i % len(container_materials)]}-{j}"
                container = Container(container_material=container_material, container_location=container_location, plant_id=plant.plant_id)
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


def create_plant_image(plant_id, image_path, plant_image_name):
    plant_image = PlantImage(plant_id=plant_id, image_path=image_path, plant_image_name=plant_image_name)
    # Add the new plant image to the session and commit
    session.add(plant_image)
    session.commit()
