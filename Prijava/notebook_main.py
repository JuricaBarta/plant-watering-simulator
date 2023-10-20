import tkinter as tk
from tkinter import ttk

from PyPosude.gui_posude import ContainersScreen
from PyPosude.detalji_posude import ContainerDetails
from biljke.gui_biljke import PlantsScreen
from biljke.detalji_bilja import PlantDetails

from crud import *
from database import *

class MainScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Algebra")
        self.geometry("1000x900")

        self.notebook = ttk.Notebook(self)
        tab1 = ContainersScreen(self.notebook, self)
        tab2 = ContainerDetails(self.notebook)
        tab3 = PlantsScreen(self.notebook, self)
        tab4 = PlantDetails(self.notebook)

        self.notebook.add(tab1, text="Posude")
        self.notebook.add(tab2, text="Detalji posude")
        self.notebook.add(tab3, text="Biljke")
        self.notebook.add(tab4, text="Detalji bilja")

        self.notebook.pack(fill="both", expand=True)

        # Add tab1 and tab3 objects to the children dictionary
        self.children['!tab1'] = tab1
        self.children['!tab3'] = tab3

    def switch_to_tab2(self, container_name):
        self.notebook.select(1)
        tab2 = self.notebook.nametowidget(self.notebook.tabs()[1])
        tab2.update_container_data(container_name)

    def switch_to_tab4(self, current_plant, plant_images):
        self.notebook.select(3)
        tab4 = self.notebook.nametowidget(self.notebook.tabs()[3])
        tab4.display_plant(current_plant, plant_images)

if __name__ == '__main__':
    main_screen = MainScreen()
    main_screen.mainloop()
