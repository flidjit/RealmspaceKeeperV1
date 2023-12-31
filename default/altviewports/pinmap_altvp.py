import tkinter as tk
from MetaNexusv1.default.engine.altvp import ClickAndDragViewport
from MetaNexusv1.default.engine.datatypes import PinMapPin, ui_clrs
from MetaNexusv1.default.text.macros import default_pin_paths
from MetaNexusv1.default.engine.tools import Pencil

"""
ToDo:
    * User selection target.
    * Display selected pin title.
    * Display map name.
"""


class PinMapAltVP(ClickAndDragViewport):
    def __init__(self, master=None, colors=ui_clrs,
                 campaign_editor_tab=None,
                 backdrop_image_path=None,
                 overworld_map=None,
                 gm_mode=True, pin_paths=None):
        super().__init__(master, backdrop_image_path)
        self._campaign_editor_tab = campaign_editor_tab
        self._colors = colors
        self.overworld_map = overworld_map
        self.gm_mode = gm_mode
        self.scale_object_list = []

        if not pin_paths:
            self.pin_paths = default_pin_paths
        else:
            self.pin_paths = pin_paths
        self.pin_images = {}
        self.pin_instances = {}
        self.selected_pin = None

        self.show_image(self.overworld_map.map_image_data)
        self.initialize_pin_images()
        self.initialize_map_pins()
        self.draw_map_scale()

        self.bind("<ButtonPress-1>", self.on_left_click)
        self.bind('<Control-ButtonPress-1>', self.on_ctrl_left_click)
        self.bind("<ButtonRelease-1>", self.on_left_click_release)

    def on_left_click(self, event):
        if self.responding:
            for pin in self.overworld_map.location_pins:
                b_box = self.overworld_map.location_pins[pin].pin_bound_box
                iof = self.image_offset
                if b_box[0][0]+iof[0] < event.x < b_box[1][0]+iof[0]:
                    if b_box[0][1]+iof[1] < event.y < b_box[1][1]+iof[1]:
                        self.selected_pin = self.overworld_map.location_pins[pin]
                        print(self.selected_pin.title_tag)

    def on_ctrl_left_click(self, event):
        if self.responding:
            if self.gm_mode:
                existing_pin = self.get_pin_at_location(event.x, event.y)
                if existing_pin is None:
                    self.add_new_pin(x=event.x, y=event.y)
                    print("Added a new pin to the overmap's pins and a pin image.")
                else:
                    print("There is already a pin at this location.")
            else:
                print('None.')

    def on_left_click_release(self, event):
        if self.responding:
            mx = event.x + self.image_offset[0]
            my = event.y + self.image_offset[1]
            click_string = ('clicked : \n' +
                            '   (s) (' + str(event.x) + ' , ' + str(event.y)+')' +
                            '   (m) (' + str(mx) + ' , ' + str(my) + ')')
            print(click_string)

    def on_right_click_and_drag(self, event):
        if self.responding:
            delta_x = event.x - self.start_x
            self.image_offset[0] += delta_x
            delta_y = event.y - self.start_y
            self.image_offset[1] += delta_y
            self.move(self.image_item,
                      delta_x, delta_y)
            for pin in self.pin_instances:
                self.move(self.pin_instances[pin],
                          delta_x, delta_y)
            self.start_x = event.x
            self.start_y = event.y

    def get_pin_at_location(self, x, y):
        for pin in self.overworld_map.location_pins:
            b_box = self.overworld_map.location_pins[pin].pin_bound_box
            iof = self.image_offset
            if b_box[0][0] + iof[0] < x < b_box[1][0] + iof[0] and \
                    b_box[0][1] + iof[1] < y < b_box[1][1] + iof[1]:
                return self.overworld_map.location_pins[pin]
        return None

    def add_new_pin(self, x, y, title_tag='Pin', pin_image_key='Star #1'):
        iof = self.image_offset
        pin_instance_key = '(' + str(x-iof[0]) + ', ' + str(y-iof[1]) + ')'
        if pin_instance_key not in self.overworld_map.location_pins:
            new_pin = PinMapPin(
                x=x-iof[0], y=y-iof[1], title_tag=title_tag,
                pin_image_key=pin_image_key,
                pin_instance_key=pin_instance_key,
                map_name=self.overworld_map.name)
            self.overworld_map.location_pins[pin_instance_key] = new_pin
            pin_image = self.pin_images[pin_image_key]
            self.add_pin_instance(
                pin_image, pin_instance_key,
                x, y)
            self.draw_map_scale()
            print('pin added at: ' + pin_instance_key)
        else:
            print('There is already a pin with that name.')

    def add_pin_instance(self, pin_image, pin_key, x, y):
        self.pin_instances[pin_key] = self.create_image(
            x, y, anchor='center', image=pin_image)
        self.update()

    def initialize_pin_images(self):
        for path_key in self.pin_paths:
            self.pin_images[path_key] = tk.PhotoImage(
                file=self.pin_paths[path_key])
            print('added image: ' + path_key + ' -- ' + self.pin_paths[path_key])

    def initialize_map_pins(self):
        for pin in self.overworld_map.location_pins:
            this_pin = self.overworld_map.location_pins[pin]
            x = this_pin.pin_location[0]
            y = this_pin.pin_location[1]
            pin_image = self.pin_images[this_pin.image_key]
            self.add_pin_instance(pin_image=pin_image, pin_key=pin, x=x, y=y)

    def draw_map_scale(self):
        for o in self.scale_object_list:
            self.delete(o)
        self.scale_object_list = Pencil.a_map_scale_object_list(
            self.overworld_map.map_scale_data, self, 20, 380)

    def exit_me(self):
        self._campaign_editor_tab.receive_map(
            self.overworld_map)
        self.destroy()


# root = tk.Tk()
# root.configure(width=900, height=530, bg='black')
# test = PinMapAltVP(root)
# root.mainloop()
