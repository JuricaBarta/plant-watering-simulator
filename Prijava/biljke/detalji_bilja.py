import tkinter as tk
from tkinter import ttk
import matplotlib as mb
from biljke.crud_bilja import CreateNewPlantScreen

class PlantDetails(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        label = tk.LabelFrame(self, text="Naziv biljke")
        label.grid(row=0, column=0, pady=10, padx=10)

        sensor_one = tk.Label(label, text="Senzor1")
        sensor_one.grid(row=0, column=0, pady=10, padx=10)
        sensor_two = tk.Label(label, text="Senzor2")
        sensor_two.grid(row=1, column=0, pady=10, padx=10)
        sensor_three = tk.Label(label, text="Senzor3")
        sensor_three.grid(row=2, column=0, pady=10, padx=10)
        sensor_four = tk.Label(label, text="Senzor4")
        sensor_four.grid(row=3, column=0, pady=10, padx=10)
        


        button_submit = tk.Button(self, text="Potvrdi", command=self.submit_plant)
        button_submit.grid(row=0,column=1)

    def submit_plant(self):
        # Ovde bi se implementirao kod za spremanje nove biljke u bazu podataka
        print("Nova biljka je spremljena.")

    def open_creator_window(self):
        button = tk.Button(self, text="Go to Tab 1",
                        command=self.open_new_plant_screen)
        button.grid(row=1,column=1)

    def open_new_plant_screen(self):
        create_new_plant_screen = CreateNewPlantScreen()
        create_new_plant_screen.grid(row=2,column=1)
