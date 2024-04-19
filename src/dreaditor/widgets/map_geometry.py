import math
from PyQt5.QtGui import QPainter

from PyQt5.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget
from PyQt5.QtCore import QRectF, QPointF
from PyQt5.QtGui import QColor, QPen, QBrush, QPolygonF

from dreaditor.config import get_config_data


PEN = QPen(QColor(0, 0, 0, 255), 5.0)
BRUSH = QBrush(QColor(64, 64, 64, 128))
DEFAULT_COLOR = QColor(76, 87, 91, 255)

class MapGeometry(QGraphicsItem):
    polybuf: list[QPolygonF]
    rect: QRectF
    color: QColor

    def __init__(self, verts: list[list[float]], indices: list[list[int]], color: QColor | None, z: float, parent: QGraphicsItem | None = ...):
        super().__init__(parent)

        if len(indices) % 3 != 0:
            raise ValueError("Index Buffer should be divisible by 3! len=%s", len(indices))

        self.setZValue(z)

        minimum = QPointF(math.inf, math.inf)
        maximum = QPointF(-math.inf, -math.inf)
        vbuf = []

        self.color = color if color else DEFAULT_COLOR

        # convert all verts to QPointF, get the min/max for the bounding rect
        for v in verts:
            vbuf.append(QPointF(v[0], -v[1]))

            if v[0] < minimum.x():
                minimum.setX(v[0])
            if v[0] > maximum.x():
                maximum.setX(v[0])
            if v[1] < minimum.y():
                minimum.setY(v[1])
            if v[1] > maximum.y():
                maximum.setY(v[1])
        
        # generate the polys from the index buffer
        polys = []
        for i in range(len(indices)//3):
            poly = QPolygonF()
            poly.append(vbuf[indices[i*3]])
            poly.append(vbuf[indices[i*3+1]])
            poly.append(vbuf[indices[i*3+2]])
            polys.append(poly)
        
        self.polybuf = polys
        self.vertex_buffer = vbuf

        minimum = minimum - QPointF(0.1, 0.1)
        maximum = maximum + QPointF(0.1, 0.1)
        self.rect = QRectF(minimum, maximum)

    def paint(self, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None = ...) -> None:
        if not get_config_data("paintGeometry"):
            return
        
        painter.setPen(QPen(self.color))
        painter.setBrush(QBrush(self.color))

        for poly in self.polybuf:
            painter.drawPolygon(poly)
    
    def boundingRect(self) -> QRectF:
        return self.rect