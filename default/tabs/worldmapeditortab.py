import tkinter as tk
from tkinter import ttk


class WorldMapEditorTab(tk.Frame):
    NAME = 'World Map'

    def __init__(self, notebook, aoa_window=None, *args, **kwargs):
        super().__init__(notebook, bg='black', *args, **kwargs)
        self.aoa_window = aoa_window
        self.title_lbl = tk.Label(
            self, bg='black', fg='white',
            text='World Map Editor', font=('courier', 20, 'bold'))
        self.title_lbl.place(x=10, y=10)
        t = 'Map Name: str<--->\n'
        t += 'Description: str<--->\n\n\n'
        t += 'World Map: <thumbnail image>\n'
        t += 'Chunk List: <listbox>\n'
        t += 'Selected Chunk: str<--.>\n'
        t += 'Chunk Hidden?: <True/False>\n'
        t += 'Selected Tile Location: x=<#>, y=<#>\n'
        t += 'Selected Tile Height: <#>\n'
        t += 'Selected Tile Tileset: str<--->\n'
        t += 'Selected Tile id: 0\n'
        t += 'Buttons: <Add/Remove Chunk>\n'
        t += '         <Add/Remove Tile>\n'
        t += '         <Add/Remove Tileset>\n'
        t += '         <Add/Remove Being>\n'
        t += '         <Add/Remove Decoration>\n'
        t += '         <Add/Remove Event>\n'
        t += '         <Go To Map Location>\n'
        self.todo_lbl = tk.Label(
            self, bg='black', fg='white',
            text=t, font=('courier', 12), justify=tk.LEFT)
        self.todo_lbl.place(x=10, y=60)
