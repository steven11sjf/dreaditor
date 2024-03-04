import logging

from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtCore import Qt, pyqtSlot
from mercury_engine_data_structures.formats.brfld import Brfld

from dreaditor.actor_reference import ActorRef
from dreaditor.constants import Scenario
from dreaditor.rom_manager import RomManager
from dreaditor.widgets.entity_list_tree_item import EntityListTreeWidgetItem


class EntityListTreeWidget(QTreeWidget):
    rom_manager: RomManager | None
    brfld_node: QTreeWidgetItem
    actors: list[EntityListTreeWidgetItem]

    def __init__(self, rom_manager: RomManager, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.logger = logging.getLogger(type(self).__name__)
        self.setHeaderHidden(True)

        self.rom_manager = rom_manager
        self.actors = []
    
    def OnNewScenarioSelected(self):

        # guard against no scenario selected
        if self.rom_manager.brfld is None:
            return
        
        self.clear()
        self.actors.clear()

        # add brfld data
        brfldItem = QTreeWidgetItem(["BRFLD"])
        brfldItem.setFlags(brfldItem.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
        brfldItem.setCheckState(0, Qt.CheckState.Unchecked)

        for layerName, layer in self.rom_manager.brfld.raw.Root.pScenario.items():
            if layerName in ["sLevelID", "sScenarioID", "vLayerFiles"]:
                continue
            
            layerItem = QTreeWidgetItem([layerName])
            layerItem.setFlags(layerItem.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
            layerItem.setCheckState(0, Qt.CheckState.Unchecked)
            brfldItem.addChild(layerItem)

            for sublayerName, sublayer in layer.dctSublayers.items():
                sublayerItem = QTreeWidgetItem([sublayerName])
                sublayerItem.setFlags(sublayerItem.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
                sublayerItem.setCheckState(0, Qt.CheckState.Unchecked)
                layerItem.addChild(sublayerItem)

                for actorName, actorData in sublayer.dctActors.items():
                    actorRef = ActorRef(self.rom_manager.scenario, layerName, sublayerName, actorName)
                    actorItem = EntityListTreeWidgetItem(self.rom_manager, actorData, actorRef, [actorName])
                    actorItem.setFlags(sublayerItem.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
                    actorItem.setCheckState(0, Qt.CheckState.Unchecked)
                    sublayerItem.addChild(actorItem)
                    self.actors.append(actorItem)
                
                
        
        self.addTopLevelItem(brfldItem)
        brfldItem.setExpanded(True)
        brfldItem.child(0).setExpanded(True) # always the entities layer
        self.brfld_node = brfldItem

        self.itemDoubleClicked.connect(self.onItemClicked)

    @pyqtSlot(QTreeWidgetItem, int)
    def onItemClicked(self, item: QTreeWidgetItem, col):
        if isinstance(item, EntityListTreeWidgetItem):
            actorName = item.text(0)
            sublayer = item.parent().text(0)
            layer = item.parent().parent().text(0)

            self.rom_manager.SelectNode(layer, sublayer, actorName)

    def SelectBrfldNode(self, layer: str, sublayer: str, sName: str):
        node = self.FindBrfldNode(layer, sublayer, sName)

        if node is None:
            return
        
        is_checked = node.checkState(0)
        if is_checked == Qt.CheckState.Unchecked:
            node.setCheckState(0, Qt.CheckState.Checked)
        else:
            node.setCheckState(0, Qt.CheckState.Unchecked)

    def FindBrfldNode(self, layer: str, sublayer: str, name: str):
        matching_actors = [item for item in self.actors 
                           if (item.reference.layer == layer and item.reference.sublayer == sublayer and item.reference.name == name)]
        
        if len(matching_actors) == 1:
            return matching_actors[0]
        
        self.logger.info("Node %s/%s/%s matched %i items", layer, sublayer, name, len(matching_actors))

        return None
