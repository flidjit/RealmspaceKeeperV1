import tkinter as tk
from tkinter import ttk


class EventEditorTab(tk.Frame):
    NAME = 'Event'

    def __init__(self, notebook, aoa_window=None, *args, **kwargs):
        super().__init__(notebook, *args, **kwargs)
        self.aoa_window = aoa_window
        self.label = tk.Label(self, text='Event')
        self.label.place(x=20, y=20)
