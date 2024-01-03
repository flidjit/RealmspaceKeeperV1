from tkinter import filedialog
from MetaNexusv1.default.engine.datatypes import PlayerData, CampaignData, PinMapData
from MetaNexusv1.default.engine.tools import DatTool
from MetaNexusv1.default.engine.datatypes import GameMapData
import os


class UserBot:
    """ UserBot Portfolio:
    -    Saves/Loads/handles CampaignData and PlayerData.
    -    Handles keyboard input presets. """

    def __init__(self, mother=None):
        self.mother = mother
        self.player_data = PlayerData()
        self.campaign_data = CampaignData()
        self.current_map_data = GameMapData()
        self.campaign_folder_path = ''
        self.initialize()
        self.get_campaign_folder_path()
        self.load_player_data()

    def initialize(self):
        self.configure_keys()

    def update(self):
        for i in self.player_data.cooldown:
            if self.player_data.cooldown[i] >= 0:
                self.player_data.cooldown[i] -= 1
        keys = self.player_data.key_map
        for i in keys:
            print('key check:'+i)

    def configure_keys(self):
        k = self.player_data.key_config
        for i in range(len(k)):
            self.player_data.key_map[k[i][1]] = False
            self.mother.accept(k[i][0], self.update_key_map, [k[i][1], True])
            self.mother.accept(k[i][0] + '-up', self.update_key_map, [k[i][1], True])

    def update_key_map(self, control_name, control_state):
        self.player_data.key_map[control_name] = control_state

    def save_player_data(self):
        DatTool.pickle_this(self.player_data, 'usr/player_config.pcfg')

    def load_player_data(self):
        try:
            self.player_data = DatTool.unpickled_thing('usr/player_config.pcfg')
            print("Returning player: " + self.player_data.name)
        except FileNotFoundError:
            self.player_data = PlayerData()
            self.save_player_data()

    def receive_player_data(self, player_data=None,
                            rps_key=None, game_mode=None):
        if player_data:
            self.player_data = player_data
        if rps_key:
            self.player_data.current_rps_key = rps_key
        if game_mode:
            self.player_data.game_mode = game_mode
        self.save_player_data()

    def new_campaign(self, campaign_data=None):
        if campaign_data:
            self.campaign_data = campaign_data
            self.campaign_data.gm = self.player_data.name
            self.campaign_data.rp_system = self.player_data.current_rps_key

    def save_campaign_data(self):
        self.get_campaign_folder_path()
        if not os.path.exists(self.campaign_folder_path):
            os.makedirs(self.campaign_folder_path)
        path = self.campaign_folder_path + '.cdat'
        DatTool.pickle_this(self.campaign_data, path)

    def load_campaign_data(self):
        initial_dir = 'RPS/' + self.player_data.current_rps_key
        initial_dir += '/Campaigns'
        file_path = filedialog.askopenfilename(
            initialdir=initial_dir, filetypes=[('Campaign Files', '*.cdat')])
        self.campaign_data = DatTool.unpickled_thing(file_path)

    def save_map_data(self):
        self.get_campaign_folder_path()
        m = self.current_map_data
        if m:
            path = (self.campaign_folder_path +
                    '/maps/' + m.name + '.gmap')
            DatTool.pickle_this(m, path)

    def load_map_data(self, map_name):
        self.get_campaign_folder_path()
        if map_name:
            path = (self.campaign_folder_path +
                    '/maps/' + map_name + '.gmap')
            self.current_map_data = DatTool.unpickled_thing(path)

    def get_campaign_info_string(self):
        c_info = self.campaign_data.name + '\n'
        c_info += self.campaign_data.gm + '\n'
        c_info += self.campaign_data.rp_system + '\n'
        c_info += str(self.campaign_data.fantasy_level) + '\n'
        c_info += str(self.campaign_data.technology_level) + '\n'
        c_info += self.campaign_data.world_map_key + '\n'
        c_info += self.campaign_data.current_map_key + '\n'
        c_info += str(len(self.campaign_data.pc_party)) + '\n'
        return c_info

    def get_campaign_maps(self):
        try:
            m_dir = 'RPS/'+self.player_data.current_rps_key
            m_dir += '/Campaigns/'+self.campaign_data.name+"/maps/"
            return [f for f in os.listdir(m_dir) if f.endswith('.gmap')]
        except FileNotFoundError:
            print("Directory not found")

    def get_campaign_folder_path(self):
        self.campaign_folder_path = 'RPS/' + self.campaign_data.rp_system
        self.campaign_folder_path += '/Campaigns/' + self.campaign_data.name

