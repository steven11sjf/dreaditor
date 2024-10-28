from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget

from dreaditor.widgets.actor_list_tree import ActorListTree
from dreaditor.widgets.entity_list_tree_item import EntityListTreeWidgetItem
from dreaditor.widgets.subarea_tree_item import SubareaTreeWidgetItem

if TYPE_CHECKING:
    from dreaditor.actor import Actor
    from dreaditor.widgets.actor_data_tree import ActorDataTreeWidget
    from dreaditor.widgets.collision_camera_item import CollisionCameraItem


class SubareasListTree(ActorListTree):
    cameras: list[QTreeWidget]
    actors: list[QTreeWidgetItem]
    actor_data_tree: ActorDataTreeWidget

    def __init__(self, actor_data_tree: ActorDataTreeWidget, parent: QWidget | None = ...) -> None:
        super().__init__(actor_data_tree, "Setups", parent)
        self.itemExpanded.connect(self.on_item_expanded)
        self.itemCollapsed.connect(self.on_item_collapsed)

    def on_new_scenario_selected(self):
        super().on_new_scenario_selected()
        self.cameras = []

    def add_actor(self, setup_id: str, cc_name: str, actor_layer: str, actor: Actor, cc_item: CollisionCameraItem):
        # custom handling since the cc should be a SubareaTreeWidgetItem
        setup_widget = self.select_child_of_widget_item(self.root_node, setup_id, True)

        cc_name = cc_item.name if cc_item else f"{cc_name} (No CC)"
        cc_widget = self.select_child_of_widget_item(setup_widget, cc_name, False)
        if not cc_widget:
            cc_widget = SubareaTreeWidgetItem(cc_item, cc_name, setup_widget)
            cc_widget.setFlags(cc_widget.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
            setup_widget.addChild(cc_widget)

        actor_layer_widget = self.select_child_of_widget_item(cc_widget, actor_layer, True)

        actor_item = EntityListTreeWidgetItem(actor)
        actor_layer_widget.addChild(actor_item)
        actor.add_entity_list_item(actor_item)
        return actor_item

    @Slot(QTreeWidgetItem)
    def on_item_expanded(self, item: QTreeWidgetItem):
        if isinstance(item, SubareaTreeWidgetItem):
            if item.collision_camera_item:
                item.collision_camera_item.request_enable()

    @Slot(QTreeWidgetItem)
    def on_item_collapsed(self, item: QTreeWidgetItem):
        if isinstance(item, SubareaTreeWidgetItem):
            if item.collision_camera_item:
                item.collision_camera_item.request_disable()
