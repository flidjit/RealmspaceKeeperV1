import MetaNexusv1.default.engine.datatypes as dt
from MetaNexusv1.default.engine.dynotab import DynoTab
import MetaNexusv1.default.tabs.campaigneditortab as cpt
import MetaNexusv1.default.tabs.pinmapeditortab as ppt
import MetaNexusv1.default.tabs.dicetab as dpt
import MetaNexusv1.default.tabs.helptab as hpt
import MetaNexusv1.default.tabs.minimaptab as mpt


class GMHostTabGroup(DynoTab):
    NAME = 'GM'

    def __init__(self, notebook, mother=None, *args, **kwargs):
        super().__init__(notebook, *args, **kwargs)
        self.mother = mother


class GMEditorTabGroup(DynoTab):
    NAME = 'Editor'

    def __init__(self, notebook, mother=None, *args, **kwargs):
        super().__init__(notebook, *args, **kwargs)
        self.mother = mother
        self.add_custom_tab(
            cpt.CampaignEditorTab,
            icon_path='default/tabs/img/icons/t_campaign.png')
        self.add_custom_tab(
            ppt.PinMapEditorTab,
            icon_path='default/tabs/img/icons/worldtabicon.png')


class PCTabGroup(DynoTab):
    NAME = 'PC'

    def __init__(self, notebook, mother=None, *args, **kwargs):
        super().__init__(notebook, *args, **kwargs)
        self.mother = mother


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
        self.mother.the_user.player_data.game_mode = dt.GameMode.STARTUP_
        self.change_mode_tabs()

    def disable_tabs(self):
        self.root_tab_group.disable_me()

    def enable_tabs(self):
        self.root_tab_group.enable_me()

    def change_mode_tabs(self):
        mode = self.mother.the_user.player_data.game_mode
        if mode == dt.GameMode.STARTUP_:
            self.set_startup_mode_tabs()
        elif mode == dt.GameMode.PLAYER_:
            self.set_player_mode_tabs()
        elif mode == dt.GameMode.GM_:
            self.set_gm_mode_tabs()

    def set_startup_mode_tabs(self):
        self.root_tab_group.add_custom_tab(
            dpt.DiceTab, icon_path='default/tabs/img/icons/t_dice.png')
        self.root_tab_group.add_custom_tab(
            hpt.HelpTab, icon_path="default/tabs/img/icons/t_help.png")

    def set_player_mode_tabs(self):
        if self.root_tab_group.get_tab('Editor'):
            self.root_tab_group.remove_tab('Editor')
        self.root_tab_group.add_custom_tab(PCTabGroup)

    def set_gm_mode_tabs(self):
        if self.root_tab_group.get_tab('PC'):
            self.root_tab_group.remove_tab('PC')
        self.root_tab_group.add_custom_tab(
            GMEditorTabGroup, icon_path="default/tabs/img/icons/t_edit.png")
        self.root_tab_group.add_custom_tab(
            GMHostTabGroup, icon_path="default/tabs/img/icons/t_gm.png")


