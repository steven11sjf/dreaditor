import math

from PySide6.QtGui import QFont, QPainter, QColor, QPen
from PySide6.QtWidgets import QStyleOptionGraphicsItem, QWidget
from PySide6.QtCore import QRectF, QPointF

from dreaditor.actor import Actor

GRAPH_COLOR = QColor(255, 255, 255, 128)
TEXT_COLOR = QColor(0, 0, 0, 150)
def paint_worldgraph(actor: Actor, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None) -> QRectF:
    worldgraph = actor.getComponent("CWorldGraph")
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

    return QRectF(topLeft, bottomRight)