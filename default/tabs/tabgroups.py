from default.tabs.campaigneditortab import CampaignEditorTab
from default.tabs.mapeditortab import MapEditorTab
from default.tabs.npceditortab import NPCEditorTab
from default.tabs.eventeditortab import EventEditorTab
from default.tabs.tablestab import TablesTab
from default.tabs.combattab import CombatTab
from default.tabs.gmactiontab import GMActionsTab
from default.tabs.gmsidebar import GMSidebarTab
from default.tabs.gmpartytab import GMPartyTab
from default.dynotab import DynoTab


class GMHostTab(DynoTab):
    NAME = 'GM'

    def __init__(self, notebook, mother=None, *args, **kwargs):
        super().__init__(notebook, *args, **kwargs)
        self.mother = mother
        self.add_custom_tab(
            GMActionsTab,
            icon_path='default/tabs/img/actiontabicon.png')
        self.add_custom_tab(
            GMPartyTab,
            icon_path='default/tabs/img/grouptabicon.png')


class GMEditorTab(DynoTab):
    NAME = 'Editor'

    def __init__(self, notebook, mother=None, *args, **kwargs):
        super().__init__(notebook, *args, **kwargs)
        self.mother = mother
        self.add_custom_tab(
            CampaignEditorTab,
            icon_path='default/tabs/img/t_campaign.png')
        self.add_custom_tab(
            MapEditorTab,
            icon_path='default/tabs/img/t_gmap.png')


class PCTab(DynoTab):
    NAME = 'PC'

    def __init__(self, notebook, mother=None, *args, **kwargs):
        super().__init__(notebook, *args, **kwargs)
        self.mother = mother

