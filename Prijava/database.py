from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import random
#from crud import generate_sensor_data

from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('sqlite:///database.db', echo=True)
Session = sessionmaker(bind=engine)
session_factory = scoped_session(Session)

# Klasa Korisnika
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

# Klasa Bilja
class Plant(Base):
    __tablename__ = "plants"

    plant_id = Column(Integer, primary_key=True)
    plant_name = Column(String, nullable=False)
    plant_image = Column(String)

    containers = relationship('Container', back_populates='plant')
    sensors = relationship('Sensor', back_populates='plant')

    def __init__(self, plant_name, plant_image=None):

        self.plant_name = plant_name
        self.plant_image = plant_image


class Container(Base):
    __tablename__ = "containers"

    container_id = Column(Integer, primary_key=True)
    location = Column(String, nullable=False)
    plant_id = Column(Integer, ForeignKey('plants.plant_id'))
    plant = relationship('Plant', back_populates='containers')
    sensors = relationship('Sensor', back_populates='container')

    def __init__(self, location, plant_name):
        plant = session.query(Plant).filter_by(plant_name=plant_name).first()
        if plant is None:
            plant = Plant(plant_name="Acer")
            session.add(plant)
            session.commit()

        self.location = location
        self.plant = plant



class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True)
    plant_id = Column(Integer, ForeignKey('plants.plant_id'))
    sensor_type = Column(String, nullable=False)
    sensor_location = Column(String, nullable=False)
    plant = relationship('Plant', back_populates='sensors')
    container_id = Column(Integer, ForeignKey('containers.container_id'))
    container = relationship('Container', back_populates='sensors')
    moisture = Column(Float)
    light = Column(Float)
    substrate_recommendation = Column(String)

    def __init__(self, sensor_type, sensor_location, container, moisture, light, substrate_recommendation):
        self.sensor_type = sensor_type
        self.sensor_location = sensor_location
        self.container = container
        self.plant = container.plant
        self.moisture = moisture
        self.light = light
        self.substrate_recommendation = substrate_recommendation


# Kreiranje baze podataka i dodavanje korisnika u tablicu
engine = create_engine("sqlite:///users.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

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
    print("Tablica korisnika je već popunjena.")

    
# kreiranje 10 biljaka samo ako ih nema u bazi
plant_names = ['Acer', 'Anthurium', 'Bamboo', 'Calla', 'Davallia Fejeensis',
               'Dracena Marginata', 'Epipremnum', 'Monstera Deliciosa',
               'Pillea Elefantore', 'Spatifilum']
for plant_name in plant_names:
    plant = session.query(Plant).filter_by(plant_name=plant_name).first()
    if plant is None:
        plant = Plant(plant_name=plant_name)
        session.add(plant)
        session.commit()
        
"""plant_image =['acer.jpg', 'anthurium.jpg',  'bamboo.jpg', 'calla.jpg',
              'davallia_fejeensis.jpg',  'dracena_marginata.jpg',
              'epipremnum.jpg',  'monstera_deliciosa.jpg',
              'pillea_elefantore.jpg', 'spatifilum.jpg']"""

# kreiranje 10 posuda samo ako ih nema u bazi
locations = ['Kitchen', 'Balcony', 'Living room']
for i, plant_name in enumerate(plant_names):
    container = session.query(Container).filter_by(location=locations[i % len(locations)]).first()
    if container is None:
        container = Container(location=locations[i % len(locations)], plant_name=plant_name)
        session.add(container)
        session.commit()

        # create sensors for the newly created container
        for sensor_type in ['moisture', 'light', 'substrate']:
            sensor_location = container.location
            substrate_recommendation = f"Use a well-draining substrate for {container.plant.plant_name}"
            moisture = random.uniform(0, 100) if sensor_type == 'moisture' else None
            light = random.uniform(0, 2000) if sensor_type == 'light' else None

            if sensor_type == 'substrate':
                if random.random() < 0.5:
                    substrate_recommendation = "Add fertilizer"
                else:
                    substrate_recommendation = "None"

            sensor = Sensor(sensor_type=sensor_type,
                            sensor_location=sensor_location,
                            container=container,
                            moisture=moisture,
                            light=light,
                            substrate_recommendation=substrate_recommendation)

            session.add(sensor)
            session.commit()



