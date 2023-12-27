import os
import platform
import sys
from tkinter import ttk
from default.engine.datatypes import ui_clrs


def get_basic_style(gui_colors=ui_clrs):
    style = ttk.Style()
    style.theme_use('alt')

    style.map(
        'TNotebook.Tab',
        background=[('selected', gui_colors['Bright #2'])])
    style.configure(
        'TNotebook.Tab',
        padding=(0, 0),
        borderwidth=0,
        highlightthickness=0,
        background=gui_colors['BG #1'],
        foreground=gui_colors['Normal #2'])
    style.configure(
        'TNotebook',
        padding=(0, 0),
        borderwidth=0,
        highlightthickness=0,
        background=gui_colors['BG #3'])
    style.configure(
        "TScrollbar",
        padding=(0, 0),
        borderwidth=0,
        highlightthickness=0,
        background=gui_colors['BG #1'],
        troughcolor=gui_colors['BG #3'],
        slidercolor=gui_colors['Normal #1'],
        arrowcolor=gui_colors['Normal #4'],
        arrowsize=15,
        sliderthickness=8)
    style.configure(
        'Treeview.Heading',
        padding=(0, 0),
        borderwidth=0,
        highlightthickness=0,
        background=gui_colors['BG #4'],
        foreground=gui_colors['Normal #4'])
    style.configure(
        'Treeview',
        padding=(0, 0),
        borderwidth=0,
        highlightthickness=0,
        fieldbackground=gui_colors['BG #3'],
        foreground=gui_colors['Normal #3'])
    style.configure(
        "TCombobox",
        padding=(0, 0),
        borderwidth=0,
        highlightthickness=0,
        background=gui_colors['BG #1'],
        selectbackground=gui_colors['BG #4'],
        foreground=gui_colors['Normal #2'],
        selectforeground=gui_colors['Normal #1'],
        arrowsize=15,
        arrowcolor=gui_colors['Bright #3'],
        font=("Arial", 12))
    style.configure(
        "TEntry",
        fieldbackground=gui_colors['BG #1'])
    return style


def serialized_image(image_path):
    try:
        with open(image_path, 'rb') as image_file:
            # Read image data as bytes
            image_data = image_file.read()
        return image_data
    except Exception as e:
        print(f"Error reading image: {e}")
        return None


class ModelHandler:
    @staticmethod
    def load_3d_map(map_data=None):
        if map_data:
            print('Load & return the map')

    @staticmethod
    def load_model(tile=None, being=None):
        if tile:
            print('load and return a tile model')
        else:
            print('No tile')
        if being:
            print('load and return a being model')
        else:
            print('No being')

    @staticmethod
    def unload_model():
        print('???')

    @staticmethod
    def swap_texture(model=None, texture_path=None):
        if model:
            if texture_path:
                print("swap this model's texture and return")


class LocalTileHandler:
    @staticmethod
    def get_tile_by_position(position=None):
        if position:
            print('retrieve the referenced tile from dict')

    @staticmethod
    def add_tile(tile=None, position=None):
        if tile:
            if position:
                print('add this tile here.')

    @staticmethod
    def delete_tile(tile_id=None):
        if tile_id:
            print('delete this tile.')

    @staticmethod
    def add_occupant(occupant=None, tile_id=None):
        if tile_id:
            if occupant:
                print('add this tile here.')

    @staticmethod
    def delete_occupant(tile_id=None):
        if tile_id:
            print('delete the occupant of this tile.')


