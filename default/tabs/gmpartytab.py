import tkinter as tk
from tkinter import ttk


class GMPartyTab(tk.Frame):
    NAME = 'PC Party'

    def __init__(self, notebook, aoa_window=None, *args, **kwargs):
        super().__init__(notebook, bg='black', *args, **kwargs)
        self.aoa_window = aoa_window
        self.title_lbl = tk.Label(
            self, bg='black', fg='white',
            text='PC Party', font=('courier', 20, 'bold'))
        self.title_lbl.place(x=10, y=10)
        t = 'Party List: {}\n'
        self.todo_lbl = tk.Label(
            self, bg='black', fg='white',
            text=t, font=('courier', 12), justify=tk.LEFT)
        self.todo_lbl.place(x=10, y=60)