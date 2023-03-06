import tkinter as tk
from tkinter import ttk

from PyPosude.gui_posude import ContainersScreen
from PyPosude.detalji_posude import ContainerDetails
from biljke.gui_biljke import PlantsScreen
from biljke.detalji_bilja import PlantDetails


class MainScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Algebra")
        self.geometry("800x600")

        notebook = ttk.Notebook(self)
        tab1 = ContainersScreen(notebook)
        tab2 = ContainerDetails(notebook)
        tab3 = PlantsScreen(notebook)
        tab4 = PlantDetails(notebook)

        notebook.add(tab1, text="Posude")
        notebook.add(tab2, text="Detalji posude")
        notebook.add(tab3, text="Biljke")
        notebook.add(tab4, text="Detalji bilja")

        notebook.pack(fill="both", expand=True)



if __name__ == '__main__':
    main_screen = MainScreen()
    main_screen.mainloop()
