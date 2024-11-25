from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import QBrush, QColor, QPainter, QPen, QPolygonF

from dreaditor.config import CurrentConfiguration
from dreaditor.utils import vector2f

if TYPE_CHECKING:
    from PySide6.QtWidgets import QStyleOptionGraphicsItem, QWidget

PEN = QPen(QColor(0, 0, 0, 255), 5.0)
BRUSH = QBrush(QColor(64, 64, 64, 128))
DEFAULT_COLOR = QColor(76, 87, 91, 255)


class MapGeometry:
    vertices: list[QPointF]
    areas: list[QRectF | QPolygonF]
    color: QColor

    def __init__(
        self,
        verts: list[list[float]],
        areas: list[dict],
        color: QColor | None,
        z: float,
    ):
        self.vertices = [vector2f(v) for v in verts]
        self.areas = []
        for a in areas:
            a_verts: list[QPointF] = [self.vertices[i] for i in a.vertices]
            if (
                len(a_verts) == 4
                and a_verts[0].x() == a_verts[1].x()
                and a_verts[2].x() == a_verts[3].x()
                and a_verts[0].y() == a_verts[3].y()
                and a_verts[1].y() == a_verts[2].y()
            ):
                self.areas.append(QRectF(a_verts[3], a_verts[1]))
            else:
                self.areas.append(QPolygonF(a_verts))

        self.color = color if color else DEFAULT_COLOR

    def paint(
        self, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None = ...
    ) -> None:
        if not CurrentConfiguration["paintGeometry"]:
            return
        painter.setPen(QPen(self.color))
        painter.setBrush(QBrush(self.color))

        for a in self.areas:
            if isinstance(a, QRectF):
                painter.drawRect(a)
            else:
                painter.drawPolygon(a)

    def paint_as_background(self, painter: QPainter | None, rect: QRectF):
        if not CurrentConfiguration["paintGeometry"]:
            return

        painter.setPen(QPen(self.color))
        painter.setBrush(QBrush(self.color))

        for a in self.areas:
            if not a.boundingRect().intersects(rect):
                continue
            if isinstance(a, QRectF):
                painter.drawRect(a)
            else:
                painter.drawPolygon(a)
