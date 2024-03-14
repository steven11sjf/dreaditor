from __future__ import annotations
from typing import TYPE_CHECKING

from enum import Enum
import logging

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QBrush, QColor

from mercury_engine_data_structures.formats.bmsad import Bmsad
from mercury_engine_data_structures.formats.bmscc import Bmscc
from mercury_engine_data_structures.file_tree_editor import FileTreeEditor

if TYPE_CHECKING:
    from dreaditor.actor_reference import ActorRef
    from dreaditor.widgets.entity_list_tree_item import EntityListTreeWidgetItem
    from dreaditor.widgets.scenario_actor_dot import ScenarioActorDot
    from dreaditor.widgets.scenario_viewer import ScenarioViewer
    from dreaditor.widgets.actor_data_tree import ActorDataTreeWidget


DOT_SIZE = 25

class ActorSelectionState(Enum):
    Toggle = 0
    Unselected = 1
    Selected = 2


class Actor:
    editor: FileTreeEditor
    ref: ActorRef
    level_data: dict
    bmsad: Bmsad | None = None
    bmscc: Bmscc | None = None

    entity_list_items: list[EntityListTreeWidgetItem]
    data_tree: ActorDataTreeWidget
    actor_dot: ScenarioActorDot | None
    actor_rect: QRectF

    isChecked: bool = True
    isSelected: bool = False

    def __init__(self, ref: ActorRef, level_data: dict, editor: FileTreeEditor, data_tree: ActorDataTreeWidget, scene: ScenarioViewer):
        self.logger = logging.getLogger(type(self).__name__)
        self.editor = editor
        self.level_data = level_data
        self.ref = ref
        self.data_tree = data_tree
        self.scene_viewer = scene
        
        bmsadLink = level_data.oActorDefLink[9:]
        
        self.entity_list_items = [] 
        self.actor_dot = None
        # Qt's y axis points down, so invert it
        self.actor_rect = QRectF(level_data.vPos[0] - DOT_SIZE, -level_data.vPos[1] - DOT_SIZE, 2 * DOT_SIZE, 2 * DOT_SIZE)

        # avoid crashing on the one broken actordef
        if bmsadLink == "actors/props/pf_mushr_fr/charclasses/pf_mushr_fr.bmsad":
            return
        
        self.bmsad = editor.get_parsed_asset(bmsadLink, type_hint=Bmsad)
        if "COLLISION" in self.bmsad.components:
            coll: str = self.bmsad.components["COLLISION"].dependencies.file
            if coll != "Unassigned":
                self.bmscc = editor.get_parsed_asset(coll.replace("\\", "/"), type_hint=Bmscc)
            else:
                self.logger.info("actor %s/%s/%s has unassigned collision file!", ref.layer, ref.sublayer, ref.name)
        
    
    def getComponent(self, name_or_type: str) -> dict | None:
        for compName, comp in self.level_data.pComponents.items():
            if compName == name_or_type:
                return comp
            if comp["@type"] == name_or_type:
                return comp
        return None

    def OnHovered(self):
        for eli in self.entity_list_items:
            pass # set bg to light gray

        # set actor_dot to be a large white oval
    

    def OnSelected(self, state: ActorSelectionState = ActorSelectionState.Toggle):
        if state == ActorSelectionState.Selected or (state == ActorSelectionState.Toggle and not self.isSelected):
            # select
            self.isSelected = True
            for eli in self.entity_list_items:
                eli.setCheckState(0, Qt.CheckState.Checked)
                pass # TODO un-bold/un-italicize

            # update scene to show change in selection
            self.actor_dot.scene().views()[0].centerOn(self.actor_dot)

            # fill in actorData
            self.data_tree.LoadActor(self)
        else:
            # unselect
            self.isSelected = False
            for eli in self.entity_list_items:
                pass # TODO un-bold/un-italicize
            self.data_tree.UnloadActor(self)

        # update scene to show change in selection
        self.actor_dot.update()
    
    def UpdateCheckState(self, state: bool):
        self.isChecked = state
        self.actor_dot.update()
        
