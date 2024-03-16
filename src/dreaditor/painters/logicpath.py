from math import sin, cos, radians

from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QPolygonF
from PyQt5.QtWidgets import QStyleOptionGraphicsItem, QWidget
from PyQt5.QtCore import QRectF, QPointF, QLineF

from dreaditor.actor import Actor


def paint_logicpath(actor: Actor, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None) -> QRectF:
    rect = QRectF()

    painter.setPen(QPen(QColor(255, 255, 255, 255), 25))
    vPos = QPointF(actor.level_data.vPos[0], -actor.level_data.vPos[1])
    lp_comp = actor.getComponent("CLogicPathComponent")
    for subpath in lp_comp.logicPath.tSubPaths:
        path: list[QLineF] = []
        prev = None
        for node in subpath.tNodes:
            curr = vPos + QPointF(node.vPos[0], -node.vPos[1])
            rect.adjust(min(curr.x(), rect.left()), min(curr.y(), rect.top()), max(curr.x(), rect.right()), max(curr.y(), rect.bottom()))
            
            if prev is None:
                prev = curr
                continue

            path.append(QLineF(prev, curr))
            prev = curr

        painter.drawLines(path)

    return rect