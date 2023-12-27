import pickle
from tkinter import filedialog

from default.engine.datatypes import PlayerData, CampaignData, OverworldMapData
import os


class UserBot:
    """ UserBot Portfolio:
    -    Saves/Loads/handles CampaignData and PlayerData.
    -    Handles keyboard input presets. """

    def __init__(self, mother=None):
        self.mother = mother
        self.player_data = PlayerData()
        self.campaign_data = CampaignData()
        self.initialize()

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
        with open('usr/player_config.pcfg', 'wb') as file:
            pickle.dump(self.player_data, file)

    def load_player_data(self):
        with open('usr/player_config.pcfg', 'rb') as file:
            self.player_data = pickle.load(file)

    def save_campaign_data(self):
        campaign_folder_path = 'RPS/' + self.campaign_data.rp_system
        campaign_folder_path += '/Campaigns/' + self.campaign_data.name
        if not os.path.exists(campaign_folder_path):
            os.makedirs(campaign_folder_path)
        path = campaign_folder_path + '.cdat'
        with open(path, 'wb') as file:
            pickle.dump(self.campaign_data, file, protocol=pickle.HIGHEST_PROTOCOL)

    def load_campaign_data(self):
        initial_dir = 'RPS/' + self.player_data.current_rps_key
        initial_dir += '/Campaigns'
        file_path = filedialog.askopenfilename(
            initialdir=initial_dir, filetypes=[('Campaign Files', '*.cdat')])
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    loaded_campaign = pickle.load(file)
                    self.campaign_data = loaded_campaign
            except Exception as e:
                print(f"Error loading campaign: {e}")

    def get_campaign_info_string(self):
        c_info = self.campaign_data.name + '\n'
        c_info += self.campaign_data.gm + '\n'
        c_info += self.campaign_data.rp_system + '\n'
        c_info += str(self.campaign_data.fantasy_level) + '\n'
        c_info += str(self.campaign_data.technology_level) + '\n'
        return c_info

    def add_campaign_headline(self):
        self.mother.announcements.receive_messages(
            new_set=self.campaign_data.headlines)

    def get_campaign_maps(self):
        try:
            m_dir = 'RPS/'+self.player_data.current_rps_key
            m_dir += '/Campaigns/'+self.campaign_data.name+"/"
            return [f for f in os.listdir(m_dir) if f.endswith('.gmap')]
        except FileNotFoundError:
            print("Directory not found")
    
    def get_campaign_filepath(self):
        rps = self.player_data.current_rps_key
        c_name = self.campaign_data.name
        return os.path.join('../../../RPS', rps, "Campaigns", c_name)

    def new_campaign(self, campaign_data=None):
        if campaign_data:
            self.campaign_data = campaign_data
            self.campaign_data.gm = self.player_data.name
            self.campaign_data.rp_system = self.player_data.current_rps_key
            save_dir = self.get_campaign_filepath() + self.campaign_data.world_map_key
            os.makedirs(save_dir)
            world_map_data = OverworldMapData(
                name=self.campaign_data.world_map_key,
                image_path=self.campaign_data.world_map_file_path)
            save_path = os.path.join(
                save_dir, self.campaign_data.world_map_key+'.gmap')
            with open(save_path, 'wb') as file:
                pickle.dump(world_map_data, file)
            self.mother.the_view.show_overworld_map(world_map_data)
