import tkinter as tk
from tkinter import filedialog
from default.datatypes import CampaignData, OverworldMapData
from default.altvp import AltViewport
from PIL import Image, ImageTk
import pickle
import os


class NewCampaignAltVP(AltViewport):
    def __init__(self, master=None, mother=None):
        super().__init__(master)
        self.mother = mother
        self.colors = self.mother.the_user.player_data.ui_colors
        self.configure(bg=self.colors['BG #4'])

        self.campaign_name_label = tk.Label(
            self, text='Campaign Name:',
            bg=self.colors['BG #4'],
            fg=self.colors['Dim #4'])
        self.campaign_name_label.place(
            x=10, y=10, width=150, height=20)
        self.campaign_name_entry = tk.Entry(
            self, bg=self.colors['BG #1'],
            fg=self.colors['Bright #1'],
            borderwidth=0,
            insertbackground=self.colors['Bright #4'],
            insertwidth=5,
            highlightcolor=self.colors['Highlight #2'],
            highlightbackground=self.colors['Highlight #1'])
        self.campaign_name_entry.place(
            x=150, y=10, width=240, height=20)

        self.world_name_label = tk.Label(
            self, text='World Name:',
            bg=self.colors['BG #4'],
            fg=self.colors['Dim #4'])
        self.world_name_label.place(
            x=400, y=10, width=150, height=20)
        self.world_name_entry = tk.Entry(
            self, bg=self.colors['BG #1'],
            fg=self.colors['Bright #1'],
            borderwidth=0,
            insertbackground=self.colors['Bright #4'],
            insertwidth=5,
            highlightcolor=self.colors['Highlight #2'],
            highlightbackground=self.colors['Highlight #1'])
        self.world_name_entry.place(
            x=550, y=10, width=240, height=20)

        self.technology_level_scale = tk.Scale(
            self, from_=0, to=5, orient=tk.HORIZONTAL,
            borderwidth=0, highlightthickness=0,
            background=self.colors['BG #3'],
            foreground=self.colors['Normal #2'],
            troughcolor=self.colors['BG #2'],
            length=200, label='Technology Level:')
        self.technology_level_scale.place(
            x=10, y=40, height=60, width=150)
        self.fantasy_level_scale = tk.Scale(
            self, from_=0, to=5, orient=tk.HORIZONTAL,
            borderwidth=0, highlightthickness=0,
            background=self.colors['BG #3'],
            foreground=self.colors['Normal #2'],
            troughcolor=self.colors['BG #2'],
            length=200, label='Fantasy Level:')
        self.fantasy_level_scale.place(
            x=10, y=110, height=60, width=150)

        self.campaign_description_lbl = tk.Label(
            self, text='Campaign Description / Headline:',
            bg=self.colors['BG #4'],
            fg=self.colors['Normal #1'])
        self.campaign_description_lbl.place(
            x=10, y=180)
        self.campaign_description_text = tk.Text(
            self, bg=self.colors['BG #1'],
            fg=self.colors['Bright #1'],
            borderwidth=0,
            insertbackground=self.colors['Bright #4'],
            insertwidth=5,
            highlightcolor=self.colors['Highlight #2'],
            highlightbackground=self.colors['Highlight #1'])
        self.campaign_description_text.place(
            x=10, y=200, width=380, height=190)

        self.create_campaign_button = tk.Button(
            self, text='Create Campaign',
            bg=self.colors['BG #3'],
            fg=self.colors['Normal #3'],
            state='disabled',
            command=self.create_new_campaign)
        self.create_campaign_button.place(
            x=640, y=360, height=30, width=150)

        self.world_map_canvas = tk.Canvas(
            self, borderwidth=0, highlightthickness=0, bg='black')
        self.world_map_canvas.place(
            x=400, y=40, height=300, width=400)
        self.map_image = None
        self.resized_map_image = None
        self.tk_image = None
        self.map_file_path = None
        self.select_world_map_button = tk.Button(
            self, text='Select a World Map',
            borderwidth=0, highlightthickness=0,
            bg=self.colors['BG #2'],
            fg=self.colors['Bright #2'],
            command=self.get_world_map)
        self.select_world_map_button.place(
            x=400, y=350, height=30, width=150)

        self.technology_level_scale.set(1)
        self.fantasy_level_scale.set(1)

    def get_world_map(self):
        self.map_file_path = filedialog.askopenfilename(
            title='Select World Map Image',
            filetypes=[("Image files", "*.png")])
        if self.map_file_path:
            self.map_image = Image.open(self.map_file_path)
            width_factor = 400 / self.map_image.width
            height_factor = 300 / self.map_image.height
            min_factor = min(width_factor, height_factor)
            self.resized_map_image = self.map_image.resize(
                (int(self.map_image.width * min_factor),
                 int(self.map_image.height * min_factor)))
            self.tk_image = ImageTk.PhotoImage(self.resized_map_image)
            self.world_map_canvas.create_image(
                0, 0, anchor=tk.NW, image=self.tk_image)
            self.world_map_canvas.image = self.map_image
            self.create_campaign_button['state'] = 'normal'

    def create_new_campaign(self):
        cn = self.campaign_name_entry.get()
        tl = self.technology_level_scale.get()
        fl = self.fantasy_level_scale.get()
        ds = self.campaign_description_text.get("1.0", tk.END)
        fp = self.map_file_path
        mk = self.world_name_entry.get()
        cp = CampaignData(
            name=cn, description=ds,
            technology_level=tl, fantasy_level=fl,
            world_map_filepath=fp, world_map_key=mk,
            current_map_key=mk)
        self.mother.the_user.new_campaign(cp)
        self.mother.the_tabs.enable_tabs()
        self.destroy()
        self.mother.the_user.save_campaign_data()

