import logging

from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget
from PySide6.QtCore import Qt, Slot

from dreaditor.actor import Actor
from dreaditor.widgets.actor_data_tree import ActorDataTreeWidget
from dreaditor.widgets.entity_list_tree_item import EntityListTreeWidgetItem


class ActorListTree(QTreeWidget):
    root_node: QTreeWidgetItem
    actors: list[EntityListTreeWidgetItem]
    actor_data_tree: ActorDataTreeWidget

    def __init__(self, actor_data_tree: ActorDataTreeWidget, root_name: str, parent: QWidget | None = ...) -> None:
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

        self.root_node = QTreeWidgetItem([root_name])
        self.root_node.setFlags(self.root_node.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
        self.root_node.setCheckState(0, Qt.CheckState.Unchecked)

        self.addTopLevelItem(self.root_node)
        self.root_node.setExpanded(True)
    
    def on_new_scenario_selected(self):
        self.actors = []
        self.root_node.takeChildren()

    def add_actor(self, path: list[str], actor: Actor) -> EntityListTreeWidgetItem:
        item = self.root_node
        for p in path:
            item = self.select_child_of_widget_item(item, p, True)
        
        actor_item = EntityListTreeWidgetItem(actor)
        item.addChild(actor_item)
        actor.add_entity_list_item(actor_item)
        return actor_item

    def select_child_of_widget_item(self, item: QTreeWidgetItem, text: str, create_if_nonexistent = False) -> QTreeWidgetItem | None:
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
