from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QFontMetricsF, QPainter, QPen, QPolygonF
from PySide6.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget

from dreaditor.config import CurrentConfiguration

COLLISION_CAMERA_COLOR = QColor(255, 200, 255, 255)
PADDING_PCT = 0.95


class CollisionCameraItem(QGraphicsItem):
    name: str
    polys: list[QPolygonF]
    bounding_rect: QRectF
    num_active_cameras: int

    def __init__(self, cc: str):
        super().__init__(None)
        self.name = cc.name
        self.polys = []
        self.bounding_rect = QRectF()
        self.num_active_cameras = 0

        pos = QPointF(cc.data.position[0], -cc.data.position[1])
        for p in cc.data.polys:
            poly = QPolygonF([pos + QPointF(pt.x, -pt.y) for pt in p.points])
            self.polys.append(poly)
            self.bounding_rect = self.bounding_rect.united(poly.boundingRect())

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = ...) -> None:
        if self.num_active_cameras > 0 or CurrentConfiguration["paintCollisionCameras"]:
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

    def request_enable(self):
        self.num_active_cameras += 1
        if self.num_active_cameras == 1:
            self.update()

        scene_view = self.scene().views()[0]
        scene_view.fitInView(self, Qt.AspectRatioMode.KeepAspectRatio)
        scene_view.scale(PADDING_PCT, PADDING_PCT)

    def request_disable(self):
        self.num_active_cameras -= 1
        if self.num_active_cameras == 0:
            self.update()
