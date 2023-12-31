import tkinter as tk
import MetaNexusv1.default.altviewports.pinmap_altvp as pvp
import MetaNexusv1.default.altviewports.startup_altvp as svp


class ViewBot:
    """ ViewBot Portfolio:
    -    Contains a viewport used to display 3-d objects.
    -    Contains an alt-viewport used to display tkinter windows.
    -    Draws the given 3-d map."""

    def __init__(self, mother=None):
        self.mother = mother
        self.campaign_folder_path = None
        self.viewport = tk.Frame(
            self.mother.mother_frame, bg='red')
        self.viewport.place(
            x=15, y=55, width=800, height=400)
        self.alt_viewport = None
        self.models = {}
        self.textures = {}
        self.cam = None
        self.cursor_3D = None

        self.display_startup_altvp(self.mother.the_user)

    def display_overworld_altvp(self, overworld_map_data=None,
                                partner=None):
        if overworld_map_data:
            self.alt_viewport = pvp.PinMapAltVP(
                master=self.mother.root,
                overworld_map=overworld_map_data)

    def display_startup_altvp(self, partner=None):
        self.alt_viewport = svp.StartupAltVP(
            master=self.mother.mother_frame,
            mother=self.mother, partner=partner)

    def update(self):
        # Perform any necessary updates in the stage
        pass

