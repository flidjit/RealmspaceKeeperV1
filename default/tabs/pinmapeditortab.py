import tkinter as tk
from tkinter import ttk

from MetaNexusv1.default.engine import tools


class PinMapEditorTab(tk.Frame):
    NAME = 'Pin Map'
    """ PinMapEditor Portfolio:
             Allows user to load an image and use it for
             a cartographic map. User can place 'pins' on the
             map in GM mode, which represent other maps. When
             the pin is clicked, user is prompted to load the map
             associated with the pin. In player mode, user can
             read lore from the map, look at logs of previous
             encounters, and replay battles. """

    def __init__(self, notebook, mother=None, *args, **kwargs):
        super().__init__(notebook, bg='black', *args, **kwargs)

        self._mother = mother
        self._view = mother.the_view
        self._user = mother.the_user
        self._tabs = mother.the_tabs
        self._chat = mother.the_chat

        self._colors = self._user.player_data.ui_colors
        self.configure(bg=self._colors['BG #3'])

        self.button_w = {}
        self.label_w = {}
        self.list_w = {}
        self.build_me()

    def build_me(self):
        d_button = [
            ['Add Pin Button', 'Bright #2', 'BG #2',
             'Add', None,
             220, 40, 50, 25],
            ['Remove Pin Button', 'Bright #2', 'BG #2',
             'Remove', None,
             220, 40, 50, 25],
            ['Link Pin Button', 'Bright #2', 'BG #2',
             'Link', None,
             220, 40, 50, 25],
            ['Un-Link Pin Button', 'Bright #2', 'BG #2',
             'Un-Link', None,
             220, 40, 50, 25]]
        d_label = [
            ['Title Label', 'BG #3', 'Dim #3',
             ('courier', 18, 'bold'), tk.LEFT,
             'Pin Map Editor', 30, 10],
            ['Pins Label', 'BG #3', 'Dim #3',
             ('Courier', 14), tk.RIGHT,
             ' ', 10, 100]]
        d_list = [
            ['Pin List', 'BG #4', 'Bright #1',
             ('Times New Roman', 12), 10, 300, 198, 400]]
        tools.TkTool.add_widgets(
            self, self._colors, button_w=d_button, label_w=d_label, list_w=d_list)
