from tkinter import ttk
from ..Styles import PAD5
from .table_area import TableArea
from OTPControllers import Controller


class Layout(ttk.Frame):
    def __init__(self, container: ttk.Frame, controller: Controller):
        super().__init__(container)

        self.table_area = TableArea(self, controller)
        self.table_area.grid(sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

