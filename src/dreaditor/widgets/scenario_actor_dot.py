import logging
from PyQt5.QtGui import QPainter

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsEllipseItem, QGraphicsItem, QGraphicsSceneHoverEvent, QGraphicsSceneMouseEvent, QStyleOptionGraphicsItem, QWidget
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QColor, QPen, QBrush

from dreaditor.actor import Actor


COLOR_ENTITY = QColor(0, 255, 0, 128)
COLOR_SOUND = QColor(143, 0, 255, 128)
COLOR_LIGHT = QColor(255, 215, 0, 128)
COLOR_UNDEFINED = QColor(0, 0, 0, 255)

OUTLINE_SELECTED = QColor(255, 0, 0, 255)
OUTLINE_HOVERED = QColor(255, 255, 255, 255)
OUTLINE_UNSELECTED = QColor(0, 0, 0, 0)
OUTLINE_WIDTH = 25

class ScenarioActorDot(QGraphicsEllipseItem):
    actor: Actor
    base_color: QColor

    def __init__(self, actor: Actor, parent: QGraphicsItem | None = ...) -> None:
        super().__init__(parent)
        self.setZValue(100)

        pen = QPen(OUTLINE_UNSELECTED)
        pen.setWidthF(10.0)
        self.setPen(pen)

        layer = actor.ref.layer
        if layer == "rEntitiesLayer":
            self.base_color = COLOR_ENTITY
        elif layer == "rSoundsLayer":
            self.base_color = COLOR_SOUND
        elif layer == "rLightsLayer":
            self.base_color = COLOR_LIGHT
        else:
            self.base_color = COLOR_UNDEFINED

        self.setRect(actor.actor_rect)
        self.actor = actor
        self.setAcceptHoverEvents(True)
    
    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent | None) -> None:
        self.setToolTip(f"{self.actor.ref.layer}/{self.actor.ref.sublayer}/{self.actor.ref.name}\n"
                        + f"{self.actor.level_data.vPos[0]}, {self.actor.level_data.vPos[1]}")
    
    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        if self.actor.isSelected:
            self.actor.OnUnselected()
        else:
            self.actor.OnSelected()
    
    def paint(self, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None = ...) -> None:
        painter.setBrush(self.base_color)

        pen = QPen(OUTLINE_SELECTED if self.actor.isSelected else OUTLINE_UNSELECTED)
        pen.setWidthF(OUTLINE_WIDTH)
        painter.setPen(pen)
        
        painter.drawEllipse(self.actor.actor_rect)