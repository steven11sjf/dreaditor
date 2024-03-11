from __future__ import annotations
from typing import TYPE_CHECKING

import logging

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QBrush, QColor

from mercury_engine_data_structures.formats.bmsad import Bmsad
from mercury_engine_data_structures.file_tree_editor import FileTreeEditor

if TYPE_CHECKING:
    from dreaditor.actor_reference import ActorRef
    from dreaditor.widgets.entity_list_tree_item import EntityListTreeWidgetItem
    from dreaditor.widgets.scenario_actor_dot import ScenarioActorDot
    from dreaditor.widgets.actor_data_tree import ActorDataTreeWidget


DOT_SIZE = 50

class Actor:
    ref: ActorRef
    level_data: dict
    bmsad: Bmsad

    entity_list_items: list[EntityListTreeWidgetItem]
    data_tree: ActorDataTreeWidget
    actor_dot: ScenarioActorDot | None
    actor_rect: QRectF

    isSelected: bool = False

    def __init__(self, ref: ActorRef, level_data: dict, editor: FileTreeEditor, data_tree: ActorDataTreeWidget):
        self.logger = logging.getLogger(type(self).__name__)
        self.level_data = level_data
        self.ref = ref
        self.data_tree = data_tree
        
        bmsadLink = level_data.oActorDefLink[9:]

        # avoid crashing on the one broken actordef
        if bmsadLink != "actors/props/pf_mushr_fr/charclasses/pf_mushr_fr.bmsad":
            self.bmsad = editor.get_parsed_asset(bmsadLink, type_hint=Bmsad)
        else:
            self.bmsad = None
        
        self.entity_list_items = []
        self.actor_dot = None
        # Qt's y axis points down, so invert it
        self.actor_rect = QRectF(level_data.vPos[0] - DOT_SIZE, -level_data.vPos[1] - DOT_SIZE, 2 * DOT_SIZE, 2 * DOT_SIZE)
    
    def OnHovered(self):
        for eli in self.entity_list_items:
            pass # set bg to light gray

        # set actor_dot to be a large white oval
    

    def OnSelected(self):
        self.isSelected = True
        for eli in self.entity_list_items:
            eli.setCheckState(0, Qt.CheckState.Checked)

        # update scene to show change in selection
        self.actor_dot.scene().views()[0].centerOn(self.actor_dot)

        # fill in actorData
        self.data_tree.LoadActor(self)
    
    def OnUnselected(self):
        self.isSelected = False
        for eli in self.entity_list_items:
            eli.setCheckState(0, Qt.CheckState.Unchecked)

        # update scene to show change in selection
        self.actor_dot.scene().update()
        
