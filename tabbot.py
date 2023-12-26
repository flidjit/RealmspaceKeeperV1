from default.datatypes import GameMode
from default.dynotab import DynoTab
from default.tabs.helptab import HelpTab
from default.tabs.tabgroups import GMHostTab, GMEditorTab, PCTab
from default.tabs.dicetab import DiceTab


class TabBot:
    """ TabBot Portfolio:
    -    Holds all tab groups for the mother.
    -    Changes tab structure depending on the game mode & rp system. """

    def __init__(self, mother=None):
        self.mother = mother
        self.root_tab_group = DynoTab(
            self.mother.mother_frame, mother=mother)
        self.root_tab_group.place(
            x=831, y=55, width=434, height=710)
        self.mother.the_user.player_data.game_mode = GameMode.STARTUP_
        self.change_tab_modes()

    def disable_tabs(self):
        self.root_tab_group.disable_me()

    def enable_tabs(self):
        self.root_tab_group.enable_me()

    def change_tab_modes(self):
        mode = self.mother.the_user.player_data.game_mode
        if mode == GameMode.STARTUP_:
            self.set_startup_mode_tabs()
        elif mode == GameMode.PLAYER_:
            self.set_player_mode_tabs()
        elif mode == GameMode.GM_:
            self.set_edit_mode_tabs()

    def set_startup_mode_tabs(self):
        self.root_tab_group.add_custom_tab(
            DiceTab, icon_path='default/tabs/img/t_dice.png')
        self.root_tab_group.add_custom_tab(
            HelpTab, icon_path="default/tabs/img/t_help.png")

    def set_player_mode_tabs(self):
        self.root_tab_group.add_custom_tab(PCTab)

    def set_edit_mode_tabs(self):
        self.root_tab_group.add_custom_tab(
            GMEditorTab, icon_path="default/tabs/img/t_edit.png")

    def set_host_mode_tabs(self):
        self.root_tab_group.add_custom_tab(
            GMHostTab, icon_path="default/tabs/img/t_gm.png")

