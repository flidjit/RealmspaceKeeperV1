import tkinter as tk
from panda3d.core import NodePath, TextureStage

from default.altviewports.overworld_altvp import OverworldMapAltVP
from MetaNexusv1.default.engine.datatypes import TileData, BeingData
from default.altviewports.startup_altvp import StartupAltVP


class ViewBot:
    """ ViewBot Portfolio:
    -    Contains a viewport used to display 3-d objects.
    -    Contains an alt-viewport used to display tkinter windows.
    -    Draws the given 3-d map."""

    def __init__(self, mother=None):
        self.mother = mother
        self.viewport = tk.Frame(
            self.mother.mother_frame, bg='red')
        self.viewport.place(
            x=15, y=55, width=800, height=400)
        self.alt_viewport = StartupAltVP(
            self.mother.mother_frame, mother=self.mother)
        self.map_data = None
        self.models = {}
        self.textures = {}
        self.cam = None
        self.cursor_3D = None

    def load_map(self, map_data):
        print('load the stage')

    def show_overworld_map(self, overworld_map_data=None, partner=None):
        if overworld_map_data:
            self.alt_viewport = OverworldMapAltVP(
                master=self.mother.root,
                overworld_map=overworld_map_data,
                partner=partner)

    def update(self):
        # Perform any necessary updates in the stage
        pass

