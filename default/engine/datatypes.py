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
    PIN = "Overworld"
    HEX = 'Hex grid'
    GRID = "Tiled 3d Map"


class GameMapData:
    def __init__(self, name='Default Map', gm='Fox',
                 description='A Map!!'):
        self.name = name
        self.gm = gm
        self.description = description
        self.creation_date = datetime.now().strftime("%Y - %m - %d")


class PinMapPin:
    def __init__(self, x=0, y=0,
                 title_tag=None, map_name=None,
                 pin_image_key=None,
                 pin_instance_key=None,
                 note=None):
        self.title_tag = title_tag
        self.instance_key = pin_instance_key
        self.map_name = map_name
        self.image_key = pin_image_key
        self.pin_location = [x, y]
        self.pin_bound_box = [[x-20, y-20],
                              [x+20, y+20]]
        self.note = note


class PinMapScale:
    def __init__(self, scale_miles=100, pixel_width=150,
                 scale_color='black', text_color='white',
                 scale_image_data=None):
        self.scale_miles = scale_miles
        self.pixel_width = pixel_width
        self.scale_color = scale_color
        self.text_color = text_color
        self.scale_image_data = scale_image_data


class PinMapData(GameMapData):
    MAP_TYPE = MapType.PIN

    def __init__(self, name='Earth', gm='Fox',
                 image_data=None, thumbnail_image_data=None,
                 map_scale_data=PinMapScale(),
                 description='A Pin Map!'):
        super().__init__(name=name, gm=gm, description=description)
        self.map_scale_data = map_scale_data
        self.map_image_data = image_data
        self.thumbnail_image_data = thumbnail_image_data
        self.location_pins = {}


class TiledMapData(GameMapData):
    MAP_TYPE = MapType.GRID

    def __init__(self):
        super().__init__()
        self.tiles = {}


class LocalMapData(TiledMapData):
    def __init__(self):
        super().__init__()
        self.npcs = {}
        self.visible_chunks = []
        self.chunk_tile_lists = {'Chunk 1': []}


class TownMapData(TiledMapData):
    def __init__(self):
        super().__init__()
        self.structures = {}
        self.services = {}


ui_clrs = {
    'BG #1': '#20170d',
    'BG #2': '#1a1322',
    'BG #3': '#0b1418',
    'BG #4': '#1c1b0d',
    'Bright #1': '#F99325',
    'Bright #2': '#974ef9',
    'Bright #3': '#28bcea',
    'Bright #4': '#eee25c',
    'Normal #1': '#d29048',
    'Normal #2': '#7d4eba',
    'Normal #3': '#50a1ba',
    'Normal #4': '#c1b74b',
    'Dim #1': '#b88F63',
    'Dim #2': '#715596',
    'Dim #3': '#517a87',
    'Dim #4': '#989252',
    'Highlight #1': '#3e2F51',
    'Highlight #2': '#ae8150',
    'System #1': 'white',
    'System #2': 'grey',
    'Warning': '#FF7373'}


class GameMode(Enum):
    PLAYER_ = "Player Mode"
    GM_ = "GM Mode"
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
        self.ui_colors = ui_clrs


class CampaignData:
    def __init__(self,
                 name='<No Campaign Selected>',
                 gm='---',
                 rp_system='---',
                 technology_level=1,
                 fantasy_level=1,
                 description='---',
                 current_map_key='---',
                 current_map_path=None,
                 world_map_path=None,
                 world_map_key='---',
                 hq_map_path=None,
                 hq_map_key='---'):
        self.name = name
        self.gm = gm
        self.rp_system = rp_system
        self.technology_level = technology_level
        self.fantasy_level = fantasy_level
        self.description = description
        self.current_map_path = current_map_path
        self.current_map_key = current_map_key
        self.world_map_key = world_map_key
        self.world_map_path = world_map_path
        self.hq_map_key = hq_map_key
        self.hq_map_path = hq_map_path
        self.headlines = [
            " A new campaign ... ",
            " Headlines need updating! ",
            " So, what's next boss?  ",
            " Load a campaign or create a new one! "]
        self.irl_start_date = datetime.now().strftime("%Y - %m - %d")
        self.pc_party = {}

