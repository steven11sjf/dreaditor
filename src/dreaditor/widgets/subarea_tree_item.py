import logging

from PySide6.QtWidgets import QTreeWidgetItem, QGraphicsPolygonItem
from PySide6.QtGui import QPen, QColor

from dreaditor.widgets.collision_camera_item import CollisionCameraItem

class SubareaTreeWidgetItem(QTreeWidgetItem):
    collision_camera_item: CollisionCameraItem | None

    def __init__(self, cci: CollisionCameraItem | None, name: str, parent: QTreeWidgetItem | None = ...) -> None:
        super().__init__(parent, [name])
        self.collision_camera_item = cci
        