import logging

from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget
from PySide6.QtCore import Qt, Slot

from dreaditor.actor import Actor
from dreaditor.widgets.actor_data_tree import ActorDataTreeWidget
from dreaditor.widgets.entity_list_tree_item import EntityListTreeWidgetItem


class EntityListTreeWidget(QTreeWidget):
    brfld_node: QTreeWidgetItem
    actors: list[EntityListTreeWidgetItem]
    actor_data_tree: ActorDataTreeWidget

    def __init__(self, actor_data_tree: ActorDataTreeWidget, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.logger = logging.getLogger(type(self).__name__)

        self.setHeaderHidden(True)
        self.setSortingEnabled(True)
        self.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self.itemChanged.connect(self.onItemChanged)
        self.itemDoubleClicked.connect(self.onItemDoubleClicked)
        # TODO set hover state, or possibly single-click state

        self.actor_data_tree = actor_data_tree
        self.actors = []

        self.brfld_node = QTreeWidgetItem(["BRFLD"])
        self.brfld_node.setFlags(self.brfld_node.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
        self.brfld_node.setCheckState(0, Qt.CheckState.Unchecked)

        self.addTopLevelItem(self.brfld_node)
        self.brfld_node.setExpanded(True)
    
    def OnNewScenarioSelected(self):
        self.actors = []
        self.brfld_node.takeChildren()

    def addBrfldItem(self, actor: Actor):
        layerItem = self.selectChildOfWidgetItem(self.brfld_node, actor.ref.layer, True)
        sublayerItem = self.selectChildOfWidgetItem(layerItem, actor.ref.sublayer, True)
        actorItem = EntityListTreeWidgetItem(actor)
        sublayerItem.addChild(actorItem)


    def selectChildOfWidgetItem(self, item: QTreeWidgetItem, text: str, create_if_nonexistent = False) -> QTreeWidgetItem | None:
        
        for childIdx in range(item.childCount()):
            if item.child(childIdx).text(0) == text:
                return item.child(childIdx)
        
        if create_if_nonexistent:
            newChild = QTreeWidgetItem(item, [text])
            newChild.setFlags(newChild.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
            newChild.setCheckState(0, Qt.CheckState.Unchecked)
            return newChild
        
        return None
    
    @Slot(QTreeWidgetItem, int)
    def onItemChanged(self, item: QTreeWidgetItem, col):
        if isinstance(item, EntityListTreeWidgetItem):
            item.actor.UpdateCheckState(item.checkState(0) == Qt.CheckState.Checked)

    @Slot(QTreeWidgetItem, int)
    def onItemDoubleClicked(self, item:  QTreeWidgetItem, col):
        if isinstance(item,  EntityListTreeWidgetItem):
            item.actor.OnSelected()
    
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
