import tkinter as tk
import os
import MetaNexusv1.default.altviewports as avps
from MetaNexusv1.default.engine import tools


class CampaignEditorTab(tk.Frame):
    NAME = 'Campaign'
    """ PinMapEditor Portfolio:
            Allows user to load and edit campaigns, and their 
            associated maps. Serves as central hub for all other 'editor' 
            tabs, which allow user in GM mode to create their world."""

    def __init__(self, notebook, mother=None,
                 *args, **kwargs):
        super().__init__(notebook, highlightthickness=0, borderwidth=0,
                         *args, **kwargs)
        self._mother = mother
        self._view = mother.the_view
        self._user = mother.the_user
        self._tabs = mother.the_tabs
        self._chat = mother.the_chat

        self._colors = self._user.player_data.ui_colors
        self.configure(bg=self._colors['BG #3'])

        self.button_w = {}
        self.label_w = {}
        self.list_w = {}
        self.build_me()

        self.info_str = ''
        self.field_str = ''
        self.display_campaign_fields()
        self.display_campaign_info()

    def build_me(self):
        d_button = [
            ['Load Campaign Button', 'Bright #2', 'BG #2',
             'Load', self.load_campaign_btn_click,
             220, 40, 50, 25],

            ['New Campaign Button', 'Bright #3', 'BG #3',
             'New', self.new_campaign_btn_click,
             280, 40, 50, 25],

            ['Save Campaign Button', 'Bright #1', 'BG #3',
             'Save', self.save_campaign_btn_click,
             370, 40, 50, 25],

            ['Load Map Button', 'Bright #3', 'BG #1',
             'Load', self.load_map_btn_click,
             110, 500, 80, 30],

            ['New Map Button', 'Bright #3', 'BG #1',
             'New', self.new_map_btn_click,
             20, 500, 80, 30],

            ['Delete Map Button', 'Bright #3', 'BG #1',
             'Delete', self.delete_map_btn_click,
             250, 500, 80, 30]]
        d_label = [
            ['Title Label', 'BG #3', 'Dim #3',
             ('courier', 18, 'bold'), tk.LEFT,
             'Campaign Editor', 30, 10],

            ['Fields Label', 'BG #3', 'Dim #3',
             ('Times New Roman', 12), tk.RIGHT,
             ' ', 10, 100],

            ['Info Label', 'BG #3', 'Bright #1',
             ('Times New Roman', 12), tk.LEFT,
             'Campaign Editor', 170, 100]]
        d_list = [
            ['Map List', 'BG #4', 'Bright #1',
             ('Times New Roman', 12), 10, 300, 198, 400]]
        tools.TkTool.add_widgets(
            self, self._colors, button_w=d_button, label_w=d_label, list_w=d_list)

    def disable_me(self):
        for s in self.button_w:
            self.button_w[s].config(state='disabled')

    def enable_me(self):
        for s in self.button_w:
            self.button_w[s].config(state='normal')
        self.display_campaign_info()

    def display_campaign_info(self):
        self.info_str = self._user.get_campaign_info_string()
        self.label_w["Info Label"].config(text=self.info_str)

    def display_campaign_fields(self):
        self.field_str = 'Campaign Name:\nGM:\nRPG System:\nTechnology Level:\n'
        self.field_str += 'Fantasy Level:\nWorld Map:\nCurrent Map:\n'
        self.field_str += '# of players:\nDescription Headline:\n'
        self.label_w['Fields Label'].config(text=self.field_str)

    def save_campaign_btn_click(self):
        self._user.save_campaign_data()
        self.populate_location_list()

    def load_campaign_btn_click(self):
        self._user.load_campaign_data()
        self.populate_location_list()
        self.display_campaign_info()

    def new_campaign_btn_click(self):
        self._view.alt_viewport = avps.newcampaign_altvp.NewCampaignAltVP(
            self._mother.root, self._mother, self)
        self._tabs.disable_tabs()

    def new_map_btn_click(self):
        self._view.alt_viewport = avps.newmap_altvp.NewMapAltVP(
            self._mother.root, self._mother, self)
        self._tabs.disable_tabs()

    def load_map_btn_click(self):
        if self.list_w['Map List'].curselection():
            if self._view.alt_viewport:
                self._view.alt_viewport.exit_me()
            selected_index = self.list_w['Map List'].curselection()
            selected_item = self.list_w['Map List'].get(selected_index)
            self._user.load_map_data(selected_item)
            self._user.campaign_data.current_map_key = selected_item
            self.display_campaign_info()
            self._view.alt_viewport = avps.pinmap_altvp.PinMapAltVP(
                master=self._mother.root, colors=self._colors,
                campaign_editor_tab=self,
                overworld_map=self._user.current_map_data)

    def delete_map_btn_click(self):
        self.populate_location_list()
        print('delete selected map.')

    def populate_location_list(self):
        self.list_w['Map List'].delete(0, tk.END)
        locations = self._user.get_campaign_maps()
        if locations:
            for map_ in locations:
                key_name, extension = os.path.splitext(map_)
                self.list_w['Map List'].insert(tk.END, key_name)
                self.list_w['Map List'].update()

    def pin_map_selected(self, pin_map_data=None):
        # called by 'load_map' if the map type is 'Overworld'.
        self._view.pin_map_selected(
            pin_map_data=pin_map_data, partner=self)

    def hex_map_selected(self):
        # make sure the aoa_window.alt_viewport is None.
        # load the local stage in the primary viewport.
        print('show a local type map')

    def grid_map_selected(self):
        # make sure the aoa_window.alt_viewport is None.
        # load the local stage in the primary viewport.
        print('show a town map')

    def receive_map(self, game_map):
        self._user.current_map_data = game_map
        self._user.save_map_data()

