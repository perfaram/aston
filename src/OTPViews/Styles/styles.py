from tkinter import ttk


class MainStyle(ttk.Style):
    def __init__(self):
        super().__init__()

        self.configure('TLabel', font=('Helvetica', 11),color='red')
        self.configure('TButton', font=('Helvetica', 11),background='#d01f32')
        self.configure('TFrame',width=350)
        self.configure('red.TFrame',background='black')