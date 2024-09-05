import math

from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QStyleOptionGraphicsItem, QWidget
from PySide6.QtCore import QRectF, QPointF

from dreaditor.actor import Actor


COLOR = QColor(255, 255, 255, 128)
def paint_worldgraph(actor: Actor, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None) -> QRectF:
    worldgraph = actor.getComponent("CWorldGraph")
    nodes: dict[str, QPointF] = {}
    topLeft = QPointF(math.inf, math.inf)
    bottomRight = QPointF(-math.inf, -math.inf)
    
    painter.setPen(QPen(COLOR, 75))
    for node in worldgraph.tNodes:
        point = QPointF(node.vPos[0], -node.vPos[1])
        nodes[node.sID] = point
        painter.drawPoint(point)

        if point.x() < topLeft.x():
            topLeft.setX(point.x())
        if point.x() > bottomRight.x():
            bottomRight.setX(point.x())
        if point.y() < topLeft.y():
            topLeft.setY(point.y())
        if point.y() > bottomRight.y():
            bottomRight.setY(point.y())
    
    painter.setPen(QPen(COLOR, 25))

    for node in worldgraph.tNodes:
        for other in node.tNeighboursIds:
            painter.drawLine(nodes[node.sID], nodes[other])

    return QRectF(topLeft, bottomRight)