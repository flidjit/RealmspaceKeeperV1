import tkinter as tk
import pickle
import os

from MetaNexusv1.default.altviewports.newcampaign_altvp import NewCampaignAltVP
from MetaNexusv1.default.altviewports.pinmap_altvp import PinMapAltVP
from MetaNexusv1.default.altviewports.newmap_altvp import NewMapAltVP


class CampaignEditorTab(tk.Frame):
    NAME = 'Campaign'

    def __init__(self, notebook, mother=None, *args, **kwargs):
        super().__init__(notebook, highlightthickness=0, borderwidth=0,
                         *args, **kwargs)
        self._mother = mother
        self._user = mother.the_user
        self._player = mother.the_user.player_data
        self._campaign = mother.the_user.campaign_data

        self.colors = self._player.ui_colors
        self.configure(bg=self.colors['BG #3'])

        self.title_lbl = tk.Label(
            self, bg=self.colors['BG #3'],
            fg=self.colors['Dim #3'],
            text='Campaign Editor',
            font=('courier', 20, 'bold'))
        self.title_lbl.place(x=10, y=10)

        self.field_str = ''
        self.field_lbl = tk.Label(
            self, bg=self.colors['BG #3'],
            fg=self.colors['Dim #2'],
            text=self.field_str, font=('Times New Roman', 12),
            justify=tk.RIGHT)
        self.field_lbl.place(x=10, y=70)
        self.display_campaign_fields()

        self.info_str = ''
        self.info_lbl = tk.Label(
            self, bg=self.colors['BG #3'],
            fg=self.colors['Bright #4'],
            text=self.info_str, font=('Times New Roman', 12),
            justify=tk.LEFT)
        self.info_lbl.place(x=160, y=70)
        self.display_campaign_info()

        self.location_list = tk.Listbox(
            self, highlightthickness=0, borderwidth=0,
            bg=self.colors['BG #4'],
            fg=self.colors['Bright #1'])
        self.location_list.place(x=10, y=300, height=198, width=400)

        sleepy_buttons = [
            ['Load Campaign Button',
             'Bright #2', 'BG #2',
             'Load', self.load_campaign_btn_click,
             220, 40, 50, 25],
            ['New Campaign Button',
             'Bright #3', 'BG #3',
             'New', self.new_campaign_btn_click,
             280, 40, 50, 25],
            ['Save Campaign Button',
             'Bright #1', 'BG #3',
             'Save', self.save_campaign_btn_click,
             370, 40, 50, 25],
            ['Load Map Button',
             'Bright #3', 'BG #1',
             'Load', self.load_map_btn_click,
             110, 500, 80, 30],
            ['New Map Button',
             'Bright #3', 'BG #1',
             'New', self.new_map_btn_click,
             20, 500, 80, 30],
            ['Delete Map Button',
             'Bright #3', 'BG #1',
             'Delete', self.delete_map_btn_click,
             250, 500, 80, 30]]

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

    def enable_me(self):
        for s in self.sleepy_widgets:
            self.sleepy_widgets[s].config(state='normal')
        self.display_campaign_info()

    def display_campaign_info(self):
        self.info_str = self._mother.the_user.get_campaign_info_string()
        self.info_lbl.config(text=self.info_str)

    def display_campaign_fields(self):
        self.field_str = 'Campaign Name:\nGM:\nRPG System:\nTechnology Level:\n'
        self.field_str += 'Fantasy Level:\nWorld Map:\nCurrent Map:\n'
        self.field_str += '# of players:\nDescription Headline:\n'
        self.field_lbl.config(text=self.field_str)

    def save_campaign_btn_click(self):
        self._mother.the_user.save_campaign_data()
        self.populate_location_list()

    def load_campaign_btn_click(self):
        self._mother.the_user.load_campaign_data()
        self.populate_location_list()
        self.display_campaign_info()

    def new_campaign_btn_click(self):
        self._mother.the_view.alt_viewport = NewCampaignAltVP(
            self._mother.root, self._mother, self)
        self._mother.the_tabs.disable_tabs()

    def new_map_btn_click(self):
        self._mother.the_view.alt_viewport = NewMapAltVP(
            self._mother.root, self._mother, self)
        self._mother.the_tabs.disable_tabs()

    def load_map_btn_click(self):
        if self.location_list.curselection():
            if self._mother.the_view.alt_viewport:
                self._mother.the_view.alt_viewport.exit_me()
            selected_index = self.location_list.curselection()[0]
            selected_item = self.location_list.get(selected_index)
            self._mother.the_user.load_map_data(selected_item)
            self._mother.the_user.campaign_data.current_map_key = selected_item
            self.display_campaign_info()
            self._mother.the_view.alt_viewport = PinMapAltVP(
                self._mother.root, self._mother, self,
                overworld_map=self._mother.the_user.current_map_data)

    def receive_map(self, game_map):
        self._mother.the_user.current_map_data = game_map
        self._mother.the_user.save_map_data()

    def delete_map_btn_click(self):
        self.populate_location_list()
        print('delete selected map.')

    def populate_location_list(self):
        print('populating')
        self.location_list.delete(0, tk.END)
        locations = self._mother.the_user.get_campaign_maps()
        if locations:
            for map_ in locations:
                key_name, extension = os.path.splitext(map_)
                self.location_list.insert(tk.END, key_name)
                self.location_list.update()

    def overworld_map_selected(self, overworld_map_data=None):
        # called by 'load_map' if the map type is 'Overworld'.
        self._mother.the_view.overworld_map_selected(
            overworld_map_data=overworld_map_data, partner=self)

    def local_map_selected(self):
        # make sure the aoa_window.alt_viewport is None.
        # load the local stage in the primary viewport.
        print('show a local type map')

    def town_map_selected(self):
        # make sure the aoa_window.alt_viewport is None.
        # load the local stage in the primary viewport.
        print('show a town map')

