import tkinter as tk
from tkinter import ttk
from crud import PlantImage
from PyPosude.crud_posude import CreateNewContainerScreen
#from PyPosude.detalji_posude import ContainerDetails
import random 


        
class ContainersScreen(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.label = tk.LabelFrame(self, text="Containers Screen")
        self.label.grid(padx=10, pady=10)

        


        labelframe_acer = tk.LabelFrame(self, text="Acer")
        labelframe_acer.grid(row=0, column=0, pady=10, padx=10)

        acer_picture_in = PlantImage("acer.jpg")
        image = acer_picture_in.get_image()

        acer_button = tk.Button(labelframe_acer, image=image, command=lambda: print("Acer Button clicked"))
        acer_button.grid(row=0, column=0, pady=10, padx=10)

        acer_name_label = tk.Label(labelframe_acer, text="Acer Plant")
        acer_name_label.grid(row=0, column=1, pady=10, padx=10)


        labelframe_anthurium = tk.LabelFrame(self, text="Anturij")
        labelframe_anthurium.grid(row=0, column=1, pady=10, padx=10)

        anthurium_picture_in = PlantImage("anthurium.jpg")
        image = anthurium_picture_in.get_image()

        anthurium_button = tk.Button(labelframe_anthurium, image=image, command=lambda: print("Anturij Button clicked"))
        anthurium_button.grid(row=0, column=0, pady=10, padx=10)

        anthurium_name_label = tk.Label(labelframe_anthurium, text="Anturij Plant")
        anthurium_name_label.grid(row=0, column=1, pady=10, padx=10)


        labelframe_bamboo = tk.LabelFrame(self, text="bamboo")
        labelframe_bamboo.grid(row=1, column=0, pady=10, padx=10)

        bamboo_picture_in = PlantImage("bamboo.jpg")
        image = bamboo_picture_in.get_image()

        bamboo_button = tk.Button(labelframe_bamboo, image=image, command=lambda: print("Anturij Button clicked"))
        bamboo_button.grid(row=0, column=0, pady=10, padx=10)

        bamboo_name_label = tk.Label(labelframe_bamboo, text="Bamboo Plant")
        bamboo_name_label.grid(row=0, column=1, pady=10, padx=10)

        add_container_button = tk.Button(self, text="Dodaj novu PyPosudu", command=self.show_new_container_screen)
        add_container_button.grid(row=1, column=1)

        #self.refresh_button = tk.Button(self.label, text="Refresh", command=self.update_container_labelframes)
        #self.refresh_button.grid(row=0, column=2, sticky='nw')


    def show_new_container_screen(self):
        new_container_screen = CreateNewContainerScreen()






