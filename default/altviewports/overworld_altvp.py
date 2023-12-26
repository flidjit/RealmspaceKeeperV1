import tkinter as tk
from tkinter import filedialog
from default.altvp import ClickAndDragViewport
from default.datatypes import OverworldPin
from default.macros import default_pin_paths



class OverworldMapAltVP(ClickAndDragViewport):
    def __init__(self, master=None, backdrop_image_path=None,
                 overworld_map=None, edit_mode=False, pin_paths=None):
        super().__init__(master, backdrop_image_path)
        self.overworld_map = overworld_map
        self.edit_mode = edit_mode

        if not pin_paths:
            self.pin_paths = default_pin_paths
        else:
            self.pin_paths = pin_paths
        self.pin_images = {}
        self.pin_instances = {}
        self.selected_pin = None

        self.new_overworld_check()
        self.show_image(self.overworld_map.image_path)
        self.get_pin_images()
        self.initialize_map_pins()

        self.bind("<ButtonPress-1>", self.on_left_click)
        self.bind('<Control-ButtonPress-1>', self.on_ctrl_left_click)
        self.bind("<ButtonRelease-1>", self.on_left_click_release)

    def new_overworld_check(self):
        if self.overworld_map.image_path:
            pass
        else:
            self.overworld_map.image_path = filedialog.askopenfilename(
                title='Select World Map Image',
                filetypes=[('Image files', '*.png')])

    def on_left_click(self, event):
        if self.responding:
            for pin in self.overworld_map.location_pins:
                b_box = self.overworld_map.location_pins[pin].pin_bound_box
                iof = self.image_offset
                if b_box[0][0]+iof[0] < event.x < b_box[1][0]+iof[0]:
                    if b_box[0][1]+iof[1] < event.y < b_box[1][1]+iof[1]:
                        self.selected_pin = self.overworld_map.location_pins[pin]
                        print(self.selected_pin.pin_title)

    def on_ctrl_left_click(self, event):
        if self.responding:
            if self.edit_mode:
                existing_pin = self.get_pin_at_location(event.x, event.y)
                if existing_pin is None:
                    self.add_new_pin(event.x, event.y)
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

    def get_pin_at_location(self, x, y):
        for pin in self.overworld_map.location_pins.values():
            b_box = pin.pin_bound_box
            iof = self.image_offset
            if b_box[0][0] + iof[0] < x < b_box[1][0] + iof[0] and \
                    b_box[0][1] + iof[1] < y < b_box[1][1] + iof[1]:
                return pin
        return None

    def add_new_pin(self, x, y):
        new_pin_title = "New Pin"
        new_pin = OverworldPin(x=x, y=y, pin_title=new_pin_title)
        self.overworld_map.location_pins[new_pin_title] = new_pin
        pin_image_path = self.pin_paths.get(new_pin_title, 'rec/img/Overmap Icons/capitol2.png')
        pin_image = tk.PhotoImage(file=pin_image_path)
        self.add_pin_instance(pin_image=pin_image, x=x, y=y)

    def get_pin_images(self):
        for path in self.pin_paths:
            self.pin_images[path] = tk.PhotoImage(file=self.pin_paths[path])

    def add_pin_instance(self, pin_image=None, x=None, y=None):
        instance_name = '(' + str(x) + ', ' + str(y) + '+'
        self.pin_instances[instance_name] = self.create_image(
            x=x, y=y, anchor='center', image=pin_image)

    def initialize_map_pins(self):
        for pin_title, pin in self.overworld_map.location_pins.items():
            x, y = pin.pin_location
            pin_image_path = self.pin_paths.get(pin_title, 'path_to_default_pin_image.png')
            pin_image = tk.PhotoImage(file=pin_image_path)
            self.add_pin_instance(pin_image=pin_image, x=x, y=y)

