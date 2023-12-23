from tkinter import filedialog
from default.altvp import ClickAndDragViewport


class OverworldMapAltVP(ClickAndDragViewport):
    def __init__(self, master=None, backdrop_image_path=None,
                 overworld_map=None):
        super().__init__(master, backdrop_image_path)
        self.overworld_map = overworld_map
        self.new_overworld_check()
        self.show_image(self.overworld_map.image_path)
        print(self.overworld_map.image_path)

    def new_overworld_check(self):
        if self.overworld_map.image_path:
            pass
        else:
            self.overworld_map.image_path = filedialog.askopenfilename(
                title='Select World Map Image',
                filetypes=[('Image files', '*.png')])

