import tkinter as tk
from .Widgets import TopMenu
from .Widgets import Layout
from AppStorage.configuration import *


class MainWindow:
    def setup(self, controller):
        """
        Initialise la racine Tkinter, construit une fenêtre et le début de la hiérarchie des widgets. 
        """

        self.controller = controller
        config = Configuration.get_instance()

        self.root = tk.Tk()
        self.root.title(config.app_details["name"] + " v" + config.app_details["version"])
        self.root.geometry("") # autosize
        self.root.option_add('*tearOff', False)
        
        # barre de menus
        self.menu_bar = TopMenu(self.root, controller)
        self.root['menu'] = self.menu_bar
        
        # zone principale de la fenêtre
        self.layout = Layout(self.root, self.controller)
        self.layout.pack(expand=True, fill=tk.BOTH)

    def loop(self):
        self.root.mainloop()
