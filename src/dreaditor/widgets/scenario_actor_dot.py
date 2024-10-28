from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QGraphicsSceneHoverEvent, QGraphicsSceneMouseEvent, QStyleOptionGraphicsItem, QWidget
from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPen

from dreaditor.actor import Actor, ActorSelectionState
from dreaditor.painters.custom_painters import custom_painters


COLOR_ENTITY = QColor(0, 255, 0, 128)
COLOR_SOUND = QColor(0, 255, 255, 128)
COLOR_LIGHT = QColor(255, 215, 0, 128)
COLOR_UNDEFINED = QColor(0, 0, 0, 255)

OUTLINE_SELECTED = QColor(255, 0, 0, 255)
OUTLINE_HOVERED = QColor(255, 255, 255, 255)
OUTLINE_UNSELECTED = QColor(0, 0, 0, 0)
OUTLINE_WIDTH = 25

class ScenarioActorDot(QGraphicsEllipseItem):
    actor: Actor
    base_color: QColor
    bounding_rect: QRectF

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
        self.bounding_rect = actor.actor_rect
        self.actor = actor
        self.setAcceptHoverEvents(True)
    
    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent | None) -> None:
        self.setToolTip(f"{self.actor.ref.layer}/{self.actor.ref.sublayer}/{self.actor.ref.name}")

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        if event.button() == Qt.MouseButton.RightButton:
            # clear selection on all items below cursor if right clicked
            self.actor.OnSelected(ActorSelectionState.Unselected)
            event.ignore()
        else:
            return super().mousePressEvent(event)
        
    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        self.actor.OnSelected()
        event.ignore()
    
    def paint(self, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None = ...) -> None:
        if not self.actor.isChecked:
            return
        
        brect = custom_painters(self.actor, painter, option, widget)

        painter.setBrush(self.base_color)
        pen = QPen(OUTLINE_SELECTED if self.actor.isSelected else OUTLINE_UNSELECTED)
        pen.setWidthF(OUTLINE_WIDTH)
        painter.setPen(pen)
        
        painter.drawEllipse(self.actor.actor_rect)

        brect = brect.united(self.bounding_rect)
        if brect != self.bounding_rect:
            self.prepareGeometryChange()
            self.bounding_rect = brect
    
    def boundingRect(self) -> QRectF:
        return self.bounding_rect