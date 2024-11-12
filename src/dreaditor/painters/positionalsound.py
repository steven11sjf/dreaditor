from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import QColor, QPainter, QPainterPath, QRadialGradient

from dreaditor.painters.base_painter import BasePainterWidget

if TYPE_CHECKING:
    from PySide6.QtWidgets import QStyleOptionGraphicsItem, QWidget


class PositionalSoundWidget(BasePainterWidget):
    COLOR_MAX = QColor(0, 255, 255, 192)
    COLOR_STRONG = QColor(0, 255, 255, 128)
    COLOR_WEAK = QColor(0, 255, 255, 48)
    config_val = "paintPositionalSound"

    def _paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = ...) -> None:
        ps_comp = self.actor.getComponent("CPositionalSoundComponent")
        vPos = QPointF(self.actor.level_data.vPos[0], -self.actor.level_data.vPos[1])
        minAtt = ps_comp.fMinAtt
        maxAtt = ps_comp.fMaxAtt

        sizePoint = QPointF(maxAtt, maxAtt)
        rect = QRectF(vPos - sizePoint, vPos + sizePoint)

        gradient = QRadialGradient(vPos, maxAtt)
        gradient.setColorAt(0, self.COLOR_MAX)
        gradient.setColorAt(minAtt / maxAtt, self.COLOR_MAX)
        gradient.setColorAt(minAtt / maxAtt + 0.001, self.COLOR_STRONG)
        gradient.setColorAt(1, self.COLOR_WEAK)

        painter.setBrush(gradient)
        painter.drawEllipse(rect)

        if self.bounding_rect != rect:
            self.prepareGeometryChange()
            self.bounding_rect = rect

    def shape(self) -> QPainterPath:
        res = QPainterPath()
        res.addEllipse(self.bounding_rect)
        return res
