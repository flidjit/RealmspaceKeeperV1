import tkinter as tk
import pickle
import os

from default.altviewports.newoverworld_altvp import OverworldMapAltVP
from default.altvp import ClickAndDragViewport
from default.aoamarquee import AOAMarquee
from default.altviewports.newcampaign_altvp import NewCampaignAltVP
from tkinter import filedialog

from default.datatypes import MapType


class CampaignEditorTab(tk.Frame):
    NAME = 'Campaign'

    def __init__(self, notebook, mother=None, *args, **kwargs):
        super().__init__(notebook, highlightthickness=0, borderwidth=0,
                         *args, **kwargs)
        self.mother = mother
        self.colors = mother.the_user.player_data.ui_colors
        self.configure(bg=self.colors['BG #3'])

        self.title_lbl = tk.Label(
            self, bg=self.colors['BG #3'],
            fg=self.colors['FG #3'],
            text='Campaign Editor',
            font=('courier', 20, 'bold'))
        self.title_lbl.place(x=10, y=10)

        self.field_str = ''
        self.field_lbl = tk.Label(
            self, bg=self.colors['BG #3'],
            fg=self.colors['FG #2'],
            text=self.field_str, font=('Times New Roman', 12),
            justify=tk.RIGHT)
        self.field_lbl.place(x=10, y=70)
        self.display_campaign_fields()

        self.info_str = ''
        self.info_lbl = tk.Label(
            self, bg=self.colors['BG #3'],
            fg=self.colors['FG #4'],
            text=self.info_str, font=('Times New Roman', 12),
            justify=tk.LEFT)
        self.info_lbl.place(x=160, y=70)
        self.display_campaign_info()

        self.location_list = tk.Listbox(
            self, highlightthickness=0, borderwidth=0,
            bg=self.colors['BG #4'],
            fg=self.colors['FG #1'])
        self.location_list.place(x=10, y=300, height=198, width=433)

        sleepy_buttons = [
            ['Load Campaign Button',
             'FG #2', 'BG #2',
             'Load', self.load_campaign_btn_click,
             220, 40, 50, 25],
            ['New Campaign Button',
             'FG #3', 'BG #3',
             'New', self.new_campaign_btn_click,
             280, 40, 50, 25],
            ['Save Campaign Button',
             'FG #1', 'BG #3',
             'Save', self.save_campaign_btn_click,
             370, 40, 50, 25],
            ['Load Map Button',
             'FG #3', 'BG #1',
             'Load', self.load_map_btn_click,
             110, 500, 50, 80],
            ['New Map Button',
             'FG #3', 'BG #1',
             'New', self.new_map_btn_click,
             20, 500, 50, 80],
            ['Delete Map Button',
             'FG #3', 'BG #1',
             'Delete', self.delete_map_btn_click,
             250, 500, 50, 80]]

        self.sleepy_widgets = {}
        for sb in sleepy_buttons:
            self.sleepy_widgets[sb[0]] = tk.Button(
                self, highlightthickness=0, borderwidth=0,
                bg=self.colors[sb[1]],
                fg=self.colors[sb[2]],
                text=sb[3], command=sb[4])
            self.sleepy_widgets[sb[0]].place(
                x=sb[5],  y=sb[6],
                width=sb[7], height=sb[8])

    def disable_me(self):
        for s in self.sleepy_widgets:
            self.sleepy_widgets[s].config(state='disabled')
        self.location_list.config(state='disabled')

    def enable_me(self):
        for s in self.sleepy_widgets:
            self.sleepy_widgets[s].config(state='normal')
        self.location_list.config(state='normal')
        self.display_campaign_info()

    def display_campaign_info(self):
        self.info_str = self.mother.the_user.get_campaign_info_string()
        self.info_lbl.config(text=self.info_str)

    def display_campaign_fields(self):
        self.field_str = 'Campaign Name:\nGM:\nRPG System:\nTechnology Level:\n'
        self.field_str += 'Fantasy Level:\nWorld Map:\n# of players:\nDescription Headline:\n'
        self.field_lbl.config(text=self.field_str)

    def save_campaign_btn_click(self):
        self.mother.the_user.save_campaign_data()

    def load_campaign_btn_click(self):
        self.mother.the_user.load_campaign_data()
        self.mother.the_user.add_campaign_headline()
        self.populate_location_list()
        self.display_campaign_info()

    def new_campaign_btn_click(self):
        self.mother.the_view.alt_viewport = NewCampaignAltVP(
            self.mother.root, self.mother)
        self.mother.the_tabs.disable_tabs()

    def new_map_btn_click(self):
        # a popup to create a new map and save it.
        # refresh the list of maps in the
        # RPS/(system)/Campaigns/(campaign name)/Maps directory.
        # select, load and view the new map.
        self.populate_location_list()
        print('Create a new map.')

    def load_map_btn_click(self):
        # after the map is loaded, check it's
        # TYPE and handle it appropriately.
        campaign_path = self.mother.the_user.get_campaign_filepath()
        if self.location_list.curselection():
            selected_index = self.location_list.curselection()[0]
            selected_item = self.location_list.get(selected_index)
            file_path = os.path.join(
                campaign_path, selected_item)
            try:
                with open(file_path, 'rb') as file:
                    loaded_map = pickle.load(file)
                    # do something with loaded_map
                print(f"Loaded map from: {file_path}")
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except Exception as e:
                print(f"Error loading map: {e}")
        else:
            print("No item selected in the listbox.")

    def delete_map_btn_click(self):
        self.populate_location_list()
        print('delete selected map.')

    def populate_location_list(self):
        self.location_list.delete(0, tk.END)
        locations = self.mother.the_user.get_campaign_maps()
        for map_ in locations:
            self.location_list.insert(tk.END, map_)
            self.location_list.update()

    def overworld_map_selected(self, overworld_map_data=None):
        # called by 'load_map' if the map type is 'Overworld'.
        self.mother.the_view.overworld_map_selected(
            overworld_map_data=overworld_map_data)

    def local_map_selected(self):
        # make sure the aoa_window.alt_viewport is None.
        # load the local stage in the primary viewport.
        print('show a local type map')

    def town_map_selected(self):
        # make sure the aoa_window.alt_viewport is None.
        # load the local stage in the primary viewport.
        print('show a town map')

