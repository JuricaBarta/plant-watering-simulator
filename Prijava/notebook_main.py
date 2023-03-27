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
        tab1 = ContainersScreen(notebook,ttk.Notebook)
        tab2 = ContainerDetails(notebook, session=ContainersScreen, container_id=[])
        tab3 = PlantsScreen(notebook, notebook)
        tab4 = PlantDetails(notebook)

        notebook.add(tab1, text="Posude")
        notebook.add(tab2, text="Detalji posude")
        notebook.add(tab3, text="Biljke")
        notebook.add(tab4, text="Detalji bilja")

        notebook.pack(fill="both", expand=True)

    def show_container_details(self, container_id):
        container_details = ContainerDetails(self.notebook, session=self.session, container_id=container_id)
        self.notebook.add(container_details, text=f"Detalji posude {container_id}")
        self.notebook.select(container_details) 

    def switch_to_plant_details(self):
        self.notebook.select(3)

if __name__ == '__main__':
    main_screen = MainScreen()
    main_screen.mainloop()
