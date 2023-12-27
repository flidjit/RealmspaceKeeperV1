import tkinter as tk
from tkinter import ttk


class WorldMapEditorTab(tk.Frame):
    NAME = 'World Map'

    def __init__(self, notebook, mother=None, *args, **kwargs):
        super().__init__(notebook, bg='black', *args, **kwargs)
        self.mother = mother
        self.partner_vp = None
        self.title_lbl = tk.Label(
            self, bg='black', fg='white',
            text='World Map Editor', font=('courier', 20, 'bold'))
        self.title_lbl.place(x=10, y=10)

        self.pin_label = tk.Label(self, text=' Pins: ')
        self.pin_label.place(x=10, y=30)
        self.pin_list = tk.Listbox(self)
        self.pin_list.place(x=10, y=60)
