import tkinter as tk
from tkinter import ttk
from tkinter import W

class Historique:
    def show_historique(self, liste_connexion):
        self.root = tk.Tk()
        self.root.title("Historique")
        self.root.geometry("") # autosize
        self.root.option_add('*tearOff', False)

        self.tree = ttk.Treeview(self.root, height=10)
        self.tree.grid(row=5, column=0, columnspan=1)
        self.tree.heading("#0", text="Timestamp", anchor=W)

        for connexion in liste_connexion:
            self.tree.insert("", 0, text=connexion.timestamp)

    def close(self):
        self.root.destroy()