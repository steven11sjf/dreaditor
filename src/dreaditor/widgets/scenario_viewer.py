from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QPen, QWheelEvent
from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsView

from dreaditor.widgets.collision_camera_item import CollisionCameraItem
from dreaditor.widgets.map_geometry import MapGeometry
from dreaditor.widgets.scenario_actor_dot import ScenarioActorDot

if TYPE_CHECKING:
    from dreaditor.actor import Actor
    from dreaditor.constants import Scenario
    from dreaditor.rom_manager import RomManager
    from dreaditor.widgets.scenario_scene import ScenarioScene

DOT_RADIUS = 100
ZOOM_FACTOR = 1.25
BORDER_PADDING = 3000.0
BACKGROUND = QColor(16, 31, 54, 255)
PEN = QPen(QColor(255, 255, 255, 255))
BRUSH = QBrush(QColor(0, 0, 0, 0))
COLLISION_CAM_COLOR = QColor(255, 200, 255, 255)


class ScenarioViewer(QGraphicsView):
    rom_manager: RomManager
    mapitem: QGraphicsPixmapItem

    def __init__(self, scene: ScenarioScene, rom_manager: RomManager):
        super().__init__(scene)
        self.logger = logging.getLogger(type(self).__name__)
        self.logger.info("Initialized ScenarioViewer!")
        self.rom_manager = rom_manager
        self.setScene(scene)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setBackgroundBrush(BACKGROUND)
        self.setViewportUpdateMode(self.ViewportUpdateMode.FullViewportUpdate)

    def on_new_scenario_selected(self, scenario: Scenario):
        self.scene().clear()

    def add_actor(self, actor: Actor):
        actor.actor_dot = ScenarioActorDot(actor, None)
        self.scene().addItem(actor.actor_dot)

    def add_map_geo(self, verts: list[list[float]], indices: list[int], color: QColor | None, z: float):
        geo = MapGeometry(verts, indices, color, z, None)
        self.scene().addItem(geo)

    def add_collision_camera(self, cc: dict) -> CollisionCameraItem:
        res = CollisionCameraItem(cc)
        self.scene().addItem(res)
        return res

    def set_bounds(self, min: list[float], max: list[float]):
        self.scene().addRect(
            QRectF(
                QPointF(min[0] - BORDER_PADDING, min[1] - BORDER_PADDING),
                QPointF(max[0] + BORDER_PADDING, max[1] + BORDER_PADDING),
            ),
            PEN,
            BRUSH,
        )

    def wheelEvent(self, event: QWheelEvent | None) -> None:
        oldPos = self.mapToScene(event.position().toPoint())

        zoomFactor = ZOOM_FACTOR if event.angleDelta().y() > 0 else 1 / ZOOM_FACTOR

        self.scale(zoomFactor, zoomFactor)

        newPos = self.mapToScene(event.position().toPoint())

        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())
