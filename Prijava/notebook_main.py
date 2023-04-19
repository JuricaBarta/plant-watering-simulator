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
        self.geometry("900x700")

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

    def switch_to_tab2(self):
        self.notebook.select(1)
        #tab2 = self.notebook.nametowidget(self.notebook.tabs()[1])

    def switch_to_tab4(self):
        self.notebook.select(3)


if __name__ == '__main__':
    main_screen = MainScreen()
    main_screen.mainloop()
