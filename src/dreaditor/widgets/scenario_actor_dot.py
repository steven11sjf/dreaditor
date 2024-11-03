from __future__ import annotations

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QGraphicsEllipseItem,
    QGraphicsItem,
    QGraphicsSceneHoverEvent,
    QGraphicsSceneMouseEvent,
    QStyleOptionGraphicsItem,
    QWidget,
)

from dreaditor.actor import Actor, ActorSelectionState
from dreaditor.painters.collision import (
    BasePainterWidget,
    BmsadCollisionWidget,
    CollisionDataFileWidget,
    DoorPainterWidget,
    ShieldPainterWidget,
    TilegroupPainterWidget,
)
from dreaditor.painters.logicpath import LogicPathWidget
from dreaditor.painters.logicshape import LogicShapeWidget
from dreaditor.painters.positionalsound import PositionalSoundWidget
from dreaditor.painters.worldgraph import WorldGraphWidget

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
    painter_widgets: list[BasePainterWidget]

    def __init__(self, actor: Actor, parent: QGraphicsItem | None = ...) -> None:
        super().__init__(parent)
        self.setZValue(100)
        self.painter_widgets = []

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

    def assign_painter_widgets(self):
        for pw in self.painter_widgets:
            self.scene().removeItem(pw)

        self.painter_widgets = []

        if (
            self.actor.getComponent("CDoorLifeComponent")
            or self.actor.getComponent("CDoorEmmyFXComponent")
            or self.actor.getComponent("CDoorCentralUnitLifeComponent")
        ):
            self.painter_widgets.append(DoorPainterWidget(self.actor, self))

        elif self.actor.getComponent("CDoorShieldLifeComponent") or self.actor.getComponent("CBeamDoorLifeComponent"):
            self.painter_widgets.append(ShieldPainterWidget(self.actor, self))
        else:
            if self.actor.bmscc:
                self.painter_widgets.append(CollisionDataFileWidget(self.actor, self))

            if (
                self.actor.bmsad
                and self.actor.bmsad.components.get("COLLISION")
                and self.actor.bmsad.components.get("COLLISION").functions
            ):
                self.painter_widgets.append(BmsadCollisionWidget(self.actor, self))

        if self.actor.getComponent("CBreakableTileGroupComponent"):
            self.painter_widgets.append(TilegroupPainterWidget(self.actor, self))

        if self.actor.getComponent("CLogicShapeComponent"):
            self.painter_widgets.append(LogicShapeWidget(self.actor, self))

        if self.actor.getComponent("CLogicPathComponent"):
            self.painter_widgets.append(LogicPathWidget(self.actor, self))

        if self.actor.getComponent("CWorldGraph"):
            self.painter_widgets.append(WorldGraphWidget(self.actor, self))

        if self.actor.ref.layer == "rSoundsLayer" and self.actor.getComponent("CPositionalSoundComponent"):
            self.painter_widgets.append(PositionalSoundWidget(self.actor, self))

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent | None) -> None:
        self.setToolTip(f"{self.actor.ref.layer}/{self.actor.ref.sublayer}/{self.actor.ref.name}")

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        if not self.actor.isChecked:
            event.ignore()
            return

        if event.button() == Qt.MouseButton.RightButton:
            # clear selection on all items below cursor if right clicked
            self.actor.OnSelected(ActorSelectionState.Unselected)
            event.ignore()
        else:
            return super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        if event.button() == Qt.MouseButton.LeftButton and self.actor.isChecked:
            self.actor.OnSelected()

        event.ignore()

    def paint(
        self, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None = ...
    ) -> None:
        if not self.actor.isChecked:
            return

        painter.setBrush(self.base_color)
        pen = QPen(OUTLINE_SELECTED if self.actor.isSelected else OUTLINE_UNSELECTED)
        pen.setWidthF(OUTLINE_WIDTH)
        painter.setPen(pen)

        painter.drawEllipse(self.actor.actor_rect)

    def update(self):
        super().update()
        for pw in self.painter_widgets:
            pw.update()

    def boundingRect(self) -> QRectF:
        return self.actor.actor_rect
