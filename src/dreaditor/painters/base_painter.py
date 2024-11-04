from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import QGraphicsItem, QGraphicsSceneHoverEvent

from dreaditor.actor import ActorSelectionState
from dreaditor.config import CurrentConfiguration

if TYPE_CHECKING:
    from PySide6.QtGui import QPainter
    from PySide6.QtWidgets import QGraphicsSceneMouseEvent, QStyleOptionGraphicsItem, QWidget

    from dreaditor.actor import Actor


class BasePainterWidget(QGraphicsItem):
    bounding_rect: QRectF
    actor: Actor
    brush: QBrush
    pen: QPen
    config_val: str

    def __init__(self, actor: Actor, parent: QGraphicsItem | None = ...) -> None:
        super().__init__(parent)
        self.bounding_rect = QRectF(actor.actor_dot.bounding_rect)
        self.actor = actor
        brush_color = QColor(actor.actor_dot.base_color)
        brush_color.setAlpha(32)
        self.brush = QBrush(brush_color)
        self.pen = QPen(actor.actor_dot.base_color, 20)
        self.setAcceptHoverEvents(True)

    def is_visible(self):
        if not self.actor.isChecked:
            return False

        if self.actor.isSelected or CurrentConfiguration[self.config_val]:
            return True

        return False

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = ...) -> None:
        if self.is_visible():
            painter.setPen(self.pen)
            painter.setBrush(self.brush)
            self._paint(painter, option, widget)

    def boundingRect(self) -> QRectF:
        return self.bounding_rect

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.setToolTip(f"{self.actor.ref.layer}/{self.actor.ref.sublayer}/{self.actor.ref.name}")

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        if not self.is_visible():
            event.ignore()
            return

        if event.button() == Qt.MouseButton.RightButton:
            # clear selection on all items below cursor if right clicked
            self.actor.OnSelected(ActorSelectionState.Unselected)
            event.ignore()
        else:
            return super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        if event.button() == Qt.MouseButton.LeftButton and self.is_visible():
            self.actor.OnSelected()

        event.ignore()

    def _paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = ...) -> None:
        return NotImplementedError("Child classes must implement _paint(painter, option, widget)!")
