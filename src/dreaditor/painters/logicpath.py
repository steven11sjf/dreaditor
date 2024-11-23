from __future__ import annotations

import math
from typing import TYPE_CHECKING

from PySide6.QtCore import QLineF, QPointF, QRectF
from PySide6.QtGui import QBrush, QColor, QPainter, QPen

from dreaditor.painters.base_painter import BasePainterWidget
from dreaditor.utils import vector2f

if TYPE_CHECKING:
    from PySide6.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget

    from dreaditor.actor import Actor


class LogicPathWidget(BasePainterWidget):
    config_val = "paintLogicPaths"

    def __init__(self, actor: Actor, parent: QGraphicsItem | None = ...) -> None:
        super().__init__(actor, parent)
        self.pen = QPen(QColor(255, 255, 255, 255), 25)
        self.swarm_pen = QPen(QColor(255, 255, 255, 255), 2)
        self.brush = QBrush(QColor(255, 255, 255, 32))

    def _paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = ...) -> None:
        topLeft = QPointF(math.inf, math.inf)
        bottomRight = QPointF(-math.inf, -math.inf)

        painter.setBrush(self.brush)
        vPos = vector2f(self.actor.level_data.vPos)
        lp_comp = self.actor.getComponent("CLogicPathComponent")
        for subpath in lp_comp.logicPath.tSubPaths:
            path: list[QLineF] = []
            prev = None
            painter.setPen(self.swarm_pen)
            for node in subpath.tNodes:
                curr = vPos + vector2f(node.vPos)

                if curr.x() < topLeft.x():
                    topLeft.setX(curr.x())
                if curr.x() > bottomRight.x():
                    bottomRight.setX(curr.x())
                if curr.y() < topLeft.y():
                    topLeft.setY(curr.y())
                if curr.y() > bottomRight.y():
                    bottomRight.setY(curr.y())

                if node.fSwarmRadius > 0.0:
                    painter.drawEllipse(curr, node.fSwarmRadius, node.fSwarmRadius)

                if prev is None:
                    prev = curr
                    continue

                path.append(QLineF(prev, curr))
                prev = curr

            painter.setPen(self.pen)
            painter.drawLines(path)

        rect = QRectF(topLeft, bottomRight)
        if rect != self.bounding_rect:
            self.prepareGeometryChange()
            self.bounding_rect = rect
