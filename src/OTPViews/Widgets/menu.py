from tkinter import ttk, Menu, Tk, messagebox
from AppStorage.configuration import *
from .new_account_dialog import NewAccountDialog
from OTPControllers import Controller


class TopMenu(Menu):
    def __init__(self, container: ttk.Frame, controller: Controller):
        super().__init__(container)
        self.controller = controller
        
        # - Start a Menu Bar
        self.master = container
        # - add a filemenu to the menu bar
        self.file_menu = Menu(self)
        self.file_menu.add_command(
            label='À propos', command=self.on_about)
        self.file_menu.add_command(
            label='Quitter', command=self.master.destroy)
        self.add_cascade(
            label="Fichier", menu=self.file_menu, underline=0)

        self.edit_menu = Menu(self)
        self.edit_menu.add_command(
            label='Nouveau compte', command=self.new_account)
        self.add_cascade(
            label="Edition", menu=self.edit_menu, underline=0)

    def on_about(self):
        config = Configuration.get_instance()
        messagebox.showinfo("showinfo", "About " + config.app_details["name"], detail=f"""\
Version: {config.app_details["version"]}
{config.app_details["copyright"]} {config.app_details["author"]}
License: {config.app_details["license"]}\
    """)

    def new_account(self):
        _ = NewAccountDialog(self.controller)
