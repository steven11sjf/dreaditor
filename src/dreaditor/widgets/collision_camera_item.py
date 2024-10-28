from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import QColor, QPainter, QPen, QFont, QFontMetricsF, QPolygonF
from PySide6.QtWidgets import QGraphicsItem, QGraphicsTextItem, QStyleOptionGraphicsItem, QWidget

from dreaditor.config import get_config_data

COLLISION_CAMERA_COLOR = QColor(255, 200, 255, 255)

class CollisionCameraItem(QGraphicsItem):
    name: str
    polys: list[QPolygonF]
    is_active: bool
    bounding_rect: QRectF

    def __init__(self, cc: str):
        super().__init__(None)
        self.name = cc.name
        self.polys = []
        self.is_active = False
        self.bounding_rect = QRectF()

        pos = QPointF(cc.data.position[0], -cc.data.position[1])
        for p in cc.data.polys:
            poly = QPolygonF([pos + QPointF(pt.x, -pt.y) for pt in p.points])
            self.polys.append(poly)
            self.bounding_rect = self.bounding_rect.united(poly.boundingRect())
    
    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = ...) -> None:
        if self.is_active or get_config_data("paintCollisionCameras"):
            painter.setPen(QPen(COLLISION_CAMERA_COLOR, 20))
            font = QFont()
            font.setPointSize(100)
            painter.setFont(font)
            
            for p in self.polys:
                painter.drawPolygon(p)
            
            name_halfsize = QFontMetricsF(font).size(0, self.name) / 2
            poly_center = self.polys[0].boundingRect().center()
            painter.drawText(poly_center - QPointF(name_halfsize.width(), name_halfsize.height()), self.name)
        
    def boundingRect(self) -> QRectF:
        return self.bounding_rect
