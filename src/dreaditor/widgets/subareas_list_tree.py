import logging

from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget
from PySide6.QtCore import Qt, Slot

from dreaditor.actor import Actor
from dreaditor.widgets.actor_data_tree import ActorDataTreeWidget
from dreaditor.widgets.entity_list_tree_item import EntityListTreeWidgetItem


class SubareasListTree(QTreeWidget):
    base_node: QTreeWidgetItem
    cameras: list[QTreeWidget]
    actors: list[QTreeWidgetItem]
    actor_data_tree: ActorDataTreeWidget

    def __init__(self, actor_data_tree: ActorDataTreeWidget, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.logger = logging.getLogger(type(self).__name__)

        self.setHeaderHidden(True)
        self.setSortingEnabled(True)
        self.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self.itemChanged.connect(self.onItemChanged)
        self.itemDoubleClicked.connect(self.onItemDoubleClicked)

        self.actor_data_tree = actor_data_tree
        self.cameras = []
        self.actors = []

        self.base_node = QTreeWidgetItem(["Collision Cameras"])
        self.base_node.setFlags(self.base_node.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
        self.base_node.setCheckState(0, Qt.CheckState.Unchecked)

        self.addTopLevelItem(self.base_node)
        self.base_node.setExpanded(True)

    def on_new_scenario_selected(self):
        self.actors = []
        self.cameras = []
        self.base_node.takeChildren()

    def add_item(self, setup_id: str, cc_name: str, actor_layer: str, actor: Actor):
        setup_widget = self.selectChildOfWidgetItem(self.base_node, setup_id, True)
        cc_widget = self.selectChildOfWidgetItem(setup_widget, cc_name, True)
        actor_layer_item = self.selectChildOfWidgetItem(cc_widget, actor_layer, True)

        actor_item = EntityListTreeWidgetItem(actor)
        actor_layer_item.addChild(actor_item)
        actor.add_entity_list_item(actor_item)

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