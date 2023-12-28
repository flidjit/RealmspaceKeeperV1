import base64
import io
import os
import platform
import sys
from tkinter import ttk
from MetaNexusv1.default.engine.datatypes import ui_clrs
import pickle
from PIL import Image, ImageTk


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


class SaveLoad:
    @staticmethod
    def pickle_this(thing, path):
        if thing and path:
            # Create the directory if it doesn't exist
            directory = os.path.dirname(path)
            if not os.path.exists(directory):
                os.makedirs(directory)

            try:
                with open(path, 'wb') as file:
                    pickle.dump(thing, file, protocol=pickle.HIGHEST_PROTOCOL)
            except Exception as e:
                print(f"Error saving thing: {e}")

    @staticmethod
    def unpickled_thing(path):
        if path:
            with open(path, 'rb') as file:
                thing = pickle.load(file)
                return thing

    @staticmethod
    def serialized_image(image_path):
        try:
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
            return image_data
        except Exception as e:
            print(f"Error reading image: {e}")
            return None

    @staticmethod
    def image_to_data(img_):
        temp_path = "temp_image.png"
        img_.save(temp_path)
        with open(temp_path, "rb") as image_file:
            img_data = base64.b64encode(image_file.read())
        os.remove(temp_path)
        return img_data

    @staticmethod
    def data_to_tk(data_):
        image_data = base64.b64decode(data_)
        image = Image.open(io.BytesIO(image_data))
        return ImageTk.PhotoImage(image)


class Pencil:
    @staticmethod
    def a_map_scale_object_list(map_scale_data, canvas, screen_x=0, screen_y=0):
        scale_group = []
        scale_text = str(map_scale_data.scale_miles) + ' Mi.'
        line_length = map_scale_data.pixel_width
        scale_group.append(
            canvas.create_text(
                screen_x+line_length/2, screen_y-15,
                text=scale_text,
                fill=map_scale_data.text_color))
        scale_group.append(
            canvas.create_line(
                screen_x, screen_y,
                line_length + screen_x, screen_y,
                fill=map_scale_data.scale_color, width=2))
        scale_group.append(
            canvas.create_line(
                screen_x, screen_y-5,
                screen_x, screen_y+5,
                fill=map_scale_data.scale_color, width=2))
        scale_group.append(
            canvas.create_line(
                line_length + screen_x, screen_y-5,
                line_length + screen_x, screen_y+5,
                fill=map_scale_data.scale_color, width=2))
        return scale_group

    @staticmethod
    def a_thumbnail_image(tk_image, thumbnail_width=100, thumbnail_height=100):
        width_factor = thumbnail_width / tk_image.width
        height_factor = thumbnail_height / tk_image.height
        min_factor = min(width_factor, height_factor)
        thumbnail = tk_image.resize(
            (int(tk_image.width * min_factor),
             int(tk_image.height * min_factor)))
        return thumbnail


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


