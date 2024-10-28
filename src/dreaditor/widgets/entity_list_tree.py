import logging

from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget
from PySide6.QtCore import Qt, Slot

from dreaditor.actor import Actor
from dreaditor.widgets.actor_data_tree import ActorDataTreeWidget
from dreaditor.widgets.actor_list_tree import ActorListTree
from dreaditor.widgets.entity_list_tree_item import EntityListTreeWidgetItem


class EntityListTreeWidget(ActorListTree):
    actors: list[EntityListTreeWidgetItem]
    actor_data_tree: ActorDataTreeWidget

    def __init__(self, actor_data_tree: ActorDataTreeWidget, parent: QWidget | None = ...) -> None:
        super().__init__(actor_data_tree, "BRFLD", parent)

    def add_actor(self, actor: Actor) -> EntityListTreeWidgetItem:
        return super().add_actor([actor.ref.layer, actor.ref.sublayer], actor)
