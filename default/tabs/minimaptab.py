import tkinter as tk
from tkinter import ttk


class MiniMapTab(ttk.Frame):
    NAME = 'Minimap'

    def __init__(self, notebook, aoa_window=None, *args, **kwargs):
        super().__init__(notebook, *args, **kwargs)
        self.aoa_window = aoa_window
        self.minimap = tk.Canvas(
            self, bg='grey', highlightthickness=0, borderwidth=0)
        self.minimap.place(x=25, y=25, width=400, height=400)

    def draw_minimap(self):
        print('draw the minimap')

