import tkinter as tk
from tkinter import filedialog
from PIL import Image
import MetaNexusv1.default.engine.altvp as avp
import MetaNexusv1.default.engine.datatypes as dt
import MetaNexusv1.default.engine.tools as tlz

"""
ToDo:
    * Grid & Hex Frames.
"""


class PinMapFrame(tk.Canvas):
    def __init__(self, master, mother, partner):
        super().__init__(master, width=560, height=380)
        self.mother = mother
        self.partner = partner
        self.working_map = dt.PinMapData()
        if mother:
            self.colors = self.mother.the_user.player_data.ui_colors
        else:
            self.colors = dt.ui_clrs
        self.configure(bg=self.colors['BG #4'],
                       borderwidth=0,
                       highlightthickness=0)

        self.title = tk.Label(
            self, text='Pin Map', font=('courier', 15, 'bold'),
            bg=self.colors['BG #4'], fg=self.colors['Bright #3'])
        self.title.place(x=10, y=10)
        self.map_canvas = tk.Canvas(
            self, borderwidth=0, highlightthickness=0, bg=self.colors['BG #4'])
        self.map_canvas.place(
            x=10, y=40, height=300, width=540)

        self.big_map_image = None
        self.small_map_image = None
        self.big_map_tk = None
        self.small_map_tk = None
        self.big_map_data = None
        self.small_map_data = None
        self.big_map_object = None
        self.small_map_object = None
        self.small_map_frame = None

        self.byte_test = None

        self.scale_object_list = []
        self.scale_width_slider = None
        self.scale_range_slider = None

        self.map_file_path = None
        self.select_map_button = tk.Button(
            self, text='Select a World Map',
            borderwidth=0, highlightthickness=0,
            bg=self.colors['Dim #3'],
            fg=self.colors['Bright #1'],
            command=self.get_world_map)
        self.select_map_button.place(
            x=400, y=340, height=30, width=150)

    def prep_image(self, path):
        try:
            self.big_map_image = Image.open(path)
            self.big_map_data = tlz.DatTool.image_to_data(
                self.big_map_image)
            self.working_map.map_image_data = self.big_map_data
            self.big_map_tk = tlz.DatTool.data_to_tk(
                self.big_map_data)
            self.make_map_thumbnail()
            self.small_map_data = tlz.DatTool.image_to_data(
                self.small_map_image)
            self.working_map.thumbnail_image_data = self.small_map_data
            self.small_map_tk = tlz.DatTool.data_to_tk(
                self.small_map_data)
        except Exception as e:
            print(f"Error converting image to data: {e}")

    def tk_to_canvas(self):
        self.big_map_object = self.map_canvas.create_image(
            0, 0, anchor=tk.NW, image=self.big_map_tk)
        self.small_map_frame = self.map_canvas.create_rectangle(
            400, 0, 540, 140, fill='black', outline='purple')
        self.small_map_image = self.map_canvas.create_image(
            420, 20, anchor=tk.NW, image=self.small_map_tk)

    def get_world_map(self):
        self.map_file_path = filedialog.askopenfilename(
            title='Select World Map Image',
            filetypes=[("Image files", "*.png")])
        self.prep_image(self.map_file_path)
        self.tk_to_canvas()
        self.draw_map_scale()
        self.scale_width_slider = tk.Scale(
            self, from_=-75, to=75,
            bg=self.colors['Bright #2'],
            troughcolor=self.colors['Dim #4'],
            orient=tk.HORIZONTAL, showvalue=False,
            command=self.width_slider_changed)
        self.scale_width_slider.place(x=10, y=350, width=150, height=20)
        self.scale_range_slider = tk.Scale(
            self, from_=1, to=4,
            bg=self.colors['Bright #3'],
            troughcolor=self.colors['Dim #1'],
            orient=tk.HORIZONTAL, showvalue=False,
            command=self.range_slider_changed)
        self.scale_range_slider.place(x=170, y=350, width=100, height=20)

    def make_map_thumbnail(self):
        self.small_map_image = tlz.AltVPTool.a_thumbnail_image(
            self.big_map_image)

    def draw_map_scale(self):
        for o in self.scale_object_list:
            self.map_canvas.delete(o)
        self.scale_object_list = tlz.AltVPTool.a_map_scale_object_list(
            self.working_map.map_scale_data,
            self.map_canvas, 20, 280)

    def width_slider_changed(self, *args):
        self.working_map.map_scale_data.pixel_width = 100 + self.scale_width_slider.get()
        self.draw_map_scale()

    def range_slider_changed(self, *args):
        r = self.scale_range_slider.get()
        mi = None
        if r == 1:
            mi = 1
        elif r == 2:
            mi = 10
        elif r == 3:
            mi = 100
        elif r == 4:
            mi = 1000
        self.working_map.map_scale_data.scale_miles = mi
        self.draw_map_scale()


class NewMapAltVP(avp.AltViewport):
    def __init__(self, master=None, mother=None, partner=None):
        super().__init__(master)
        self.mother = mother
        self.partner = partner
        if mother:
            self.colors = self.mother.the_user.player_data.ui_colors
        else:
            self.colors = dt.ui_clrs
        self.configure(bg=self.colors['BG #3'])
        self.title_label = tk.Label(
            self, text='New Map', font=('courier', 20, 'bold'),
            bg=self.colors['BG #3'], fg=self.colors['Dim #2'])
        self.title_label.place(x=10, y=10)

        self.map_name_label = tk.Label(
            self, text='Map Name: ',
            bg=self.colors['BG #3'], fg=self.colors['Normal #2'])
        self.map_name_label.place(x=10, y=40)
        self.map_name_entry = tk.Entry(
            self, bg=self.colors['BG #4'], fg=self.colors['Bright #1'],
            borderwidth=0, insertwidth=5,
            insertbackground=self.colors['Bright #4'],
            highlightcolor=self.colors['Highlight #2'],
            highlightbackground=self.colors['Highlight #1'])
        self.map_name_entry.place(x=5, y=60, width=215)

        self.map_type_label = tk.Label(
            self, text='Map Type: \n    <Pin>, <Hex>, <Grid>',
            bg=self.colors['BG #3'], fg=self.colors['Normal #2'])
        self.map_type_label.place(x=10, y=100)

        self.map_description_label = tk.Label(
            self, text='Description/Headline: ',
            bg=self.colors['BG #3'], fg=self.colors['Normal #2'])
        self.map_description_label.place(x=10, y=190)
        self.map_description_text = tk.Text(
            self, bg=self.colors['BG #4'], fg=self.colors['Bright #1'],
            borderwidth=0, insertwidth=5,
            insertbackground=self.colors['Bright #4'],
            highlightcolor=self.colors['Highlight #2'],
            highlightbackground=self.colors['Highlight #1'])
        self.map_description_text.place(x=5, y=210, height=150, width=215)

        self.create_map_button = tk.Button(
            self, text='Create Map',
            borderwidth=0, highlightthickness=0,
            bg=self.colors['Dim #2'],
            fg=self.colors['Bright #4'],
            command=self.create_map)
        self.create_map_button.place(
            x=35, y=365, height=30, width=150)

        self.map_type_widget = PinMapFrame(self, mother, partner)
        self.map_type_widget.place(x=227, y=8)

    def create_map(self):
        m = self.map_type_widget.working_map
        m.name = self.map_name_entry.get()
        m.description = self.map_description_text.get('1.0', tk.END)
        self.mother.the_user.current_map_data = m
        self.mother.the_user.campaign_data.current_map_key = m.name
        self.mother.the_user.save_map_data()
        self.partner.populate_location_list()
        self.mother.the_tabs.enable_tabs()
        self.exit_me()

    def exit_me(self):
        self.destroy()


# root = tk.Tk()
# root.configure(width=900, height=530, bg='black')
# test = NewMapAltVP(root)
# root.mainloop()
