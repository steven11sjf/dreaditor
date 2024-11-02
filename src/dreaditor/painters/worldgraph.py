from __future__ import annotations

import math
from typing import TYPE_CHECKING

from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import QColor, QFont, QPainter, QPen

from dreaditor.painters.base_painter import BasePainterWidget

if TYPE_CHECKING:
    from PySide6.QtWidgets import QStyleOptionGraphicsItem, QWidget

GRAPH_COLOR = QColor(255, 255, 255, 128)
TEXT_COLOR = QColor(0, 0, 0, 150)


class WorldGraphWidget(BasePainterWidget):
    config_val = "paintWorldGraph"

    def _paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = ...) -> None:
        worldgraph = self.actor.getComponent("CWorldGraph")
        nodes: dict[str, QPointF] = {}
        topLeft = QPointF(math.inf, math.inf)
        bottomRight = QPointF(-math.inf, -math.inf)

        for node in worldgraph.tNodes:
            point = QPointF(node.vPos[0], -node.vPos[1])
            nodes[node.sID] = point

            if point.x() < topLeft.x():
                topLeft.setX(point.x())
            if point.x() > bottomRight.x():
                bottomRight.setX(point.x())
            if point.y() < topLeft.y():
                topLeft.setY(point.y())
            if point.y() > bottomRight.y():
                bottomRight.setY(point.y())

        for node in worldgraph.tNodes:
            # Draw lines
            painter.setPen(QPen(GRAPH_COLOR, 25))
            for other in node.tNeighboursIds:
                painter.drawLine(nodes[node.sID], nodes[other])

            # Draw node
            painter.setPen(QPen(GRAPH_COLOR, 75))
            painter.drawPoint(nodes[node.sID])

        # Draw node ID
        font = QFont(painter.font())
        font.setPixelSize(75)
        painter.setFont(font)
        painter.setPen(QPen(TEXT_COLOR, 75))
        for i, node in enumerate(worldgraph.tNodes):
            painter.drawText(nodes[node.sID], f"{i}: {node.sID}")

        rect = QRectF(topLeft, bottomRight)
        if rect != self.bounding_rect:
            self.prepareGeometryChange()
            self.bounding_rect = rect
