from datetime import datetime
import random
from enum import Enum


class DieRoll:
    def __init__(self, rolled_by='GM', roll_string='1d20',
                 faces=20, number=2, bonus=1,
                 rolls=None, total=0, roll_me=True):
        self.roll_string = roll_string
        self.rolled_by = rolled_by
        self.faces = faces
        self.number = number
        self.bonus = bonus
        if rolls:
            self.rolls = rolls
        else:
            self.rolls = []
        self.total = total
        if roll_me:
            self.roll_me()
        self.get_roll_string()

    def roll_me(self):
        self.rolls = []
        self.total = 0
        for _ in range(self.number):
            result = random.randint(1, self.faces)
            result += self.bonus
            self.rolls.append(result)
            self.total += result

    def get_roll_string(self):
        s = self.rolled_by + ' rolled '
        s += str(self.number) + 'd' + str(self.faces)
        s += '+' + str(self.bonus) + ': '
        if len(self.rolls) > 1:
            s += '( '
            for i in self.rolls:
                s += str(i) + ', '
            s = s[:-2]  # Remove the trailing comma and space
            s += ' ) '
        s += 'Result: ' + str(self.total)
        self.roll_string = s
        print(s)


class ModelData:
    def __init__(self, model_path, render, x, y,
                 occupant=None, walkable=False, flags=None):
        self.billboard_sprite = False
        self.node_path = None
        self.position = [0, 0]
        self.height = 0
        self.facing = 'North'
        self.render = render
        self.instance = None


class BeingData(ModelData):
    def __init__(self, model_path, render, x, y, character=None):
        super().__init__(model_path, render, x, y)
        self.character = character
        self.character_model_path = None
        self.owner = 'GM'


class TileData(ModelData):
    def __init__(self, x=1, y=1, height=0, model_path=None,
                 render=None, occupant=None,
                 decoration=None, walkable=False, flags=None):
        super().__init__(model_path, render, x, y)
        self.position = (x, y)
        self.height = height

        self.tile_sheet_path = None
        self.tile_id = None

        self.occupant = occupant
        self.walkable = walkable
        self.decoration = decoration
        self.flags = flags or []


class MapType(Enum):
    OVERWORLD = "Overworld"
    HEX = 'Hex grid'
    TOWN = "Town"
    LOCAL = "Local"


class GameMapData:
    def __init__(self, name='Default Map', gm='Fox'):
        self.name = name
        self.gm = gm
        self.creation_date = datetime.now().strftime("%Y - %m - %d")


class OverworldMapData(GameMapData):
    MAP_TYPE = MapType.OVERWORLD

    def __init__(self, name='Earth', gm='Fox',
                 image_path='rec/img/worldmap1.png',
                 pixels_per_mile=10):
        super().__init__(name=name, gm=gm)
        self.pixels_per_mile = pixels_per_mile
        self.image_path = image_path
        self.pin_locations = {}


class TiledMapData(GameMapData):
    def __init__(self):
        super().__init__()
        self.tiles = {}


class LocalMapData(TiledMapData):
    MAP_TYPE = MapType.LOCAL

    def __init__(self):
        super().__init__()
        self.npcs = {}
        self.visible_chunks = []
        self.chunk_tile_lists = {'Chunk 1': []}


class TownMapData(TiledMapData):
    MAP_TYPE = MapType.TOWN

    def __init__(self):
        super().__init__()
        self.structures = {}
        self.services = {}


ui_colors = {
    'BG #1': '#28052C',
    'BG #2': '#14092E',
    'BG #3': '#1a1322',
    'BG #4': '#0b1418',
    'FG #1': '#e58b2a',
    'FG #2': '#9b59f2',
    'FG #3': '#28bcea',
    'FG #4': '#f2e231',
    'Chat #1': 'light green',
    'Chat #2': 'pink',
    'Chat #3': 'orange',
    'Chat #4': 'yellow',
    'Chat #5': 'red',
    'Chat #6': '#31f2ee'}


class GameMode(Enum):
    PLAYER_ = "Player Mode"
    GM_ = "GM Mode"
    EDITOR_ = "Campaign Editor"
    HOST_ = "Hosting a Game"
    STARTUP_ = "Startup"


class PlayerData:
    def __init__(self):
        self.name = 'New Player'
        self.email = ''
        self.is_male = True
        self.current_rps_key = 'AOARP'
        self.current_campaign_key = 'Campaign Name'
        self.current_character_key = 'Somebody'
        self.date_joined = datetime.now().strftime("%Y - %m - %d")
        self.game_mode = GameMode.STARTUP_
        self.cooldown = {}
        self.key_map = {}
        self.key_config = {}
        self.machine_data = {
            "OS": None,
            "Machine": None,
            "System": None,
            "Release": None,
            "OpenGL Version": None,
            "Vendor": None,
            "Renderer": None}
        self.ui_colors = ui_colors


class CampaignData:
    def __init__(self,
                 name='<No Campaign Selected>',
                 gm='---',
                 rp_system='---',
                 technology_level=1,
                 fantasy_level=1,
                 description='---',
                 world_map_key='---',
                 current_map_key='---',
                 world_map_filepath=None):
        self.name = name
        self.gm = gm
        self.rp_system = rp_system
        self.technology_level = technology_level
        self.fantasy_level = fantasy_level
        self.description = description
        self.current_map_key = current_map_key
        self.world_map_key = world_map_key
        self.world_map_file_path = world_map_filepath
        self.headlines = [
            " A new campaign ... ",
            " Headlines need updating! ",
            " So, what's next boss?  ",
            " Load a campaign or create a new one! "]
        self.pc_party = {}
        self.npc_sidebar = {}
        self.irl_start_date = datetime.now().strftime("%Y - %m - %d")
        self.in_game_start_date = None
        self.in_game_current_date = None

