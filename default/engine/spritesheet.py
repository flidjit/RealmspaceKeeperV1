import tkinter as tk
import MetaNexusv1.default.engine.tools as tlz
# Not implemented !
# Not functional !


class SpriteSheet:
    def __init__(self, name='Name',
                 image_data=None, image_path=None,
                 cells=None, animations=None):
        self.name = name

        self.image_data = image_data
        if image_path:
            try:
                self.image_data = tlz.DatTool.serialized_image(image_path)
            except Exception as e:
                print('Exception:' + str(e))
                print('failed to get image data.')
        try:
            self.image = tk.PhotoImage(data=self.image_data)
        except Exception as e:
            print('Exception:' + str(e))
            print('failed to create image.')

        if not cells:
            # 'Cell id': [x1, y1, x2, y2]
            self.cells = {}
        else:
            self.cells = cells

        if not animations:
            # 'Animation id': [[cell_id, time_held]]
            self.animations = {}
        else:
            self.animations = animations

    def get_cell(self, cell_id=None):
        if cell_id:
            print('return the cell image data.')