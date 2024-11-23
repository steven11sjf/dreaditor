from __future__ import annotations

from math import cos, radians, sin
from typing import TYPE_CHECKING

from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import QPainter, QPolygonF

from dreaditor.painters.base_painter import BasePainterWidget
from dreaditor.utils import vector2f

if TYPE_CHECKING:
    from PySide6.QtWidgets import QStyleOptionGraphicsItem, QWidget


class LogicShapeWidget(BasePainterWidget):
    config_val = "paintLogicShapes"

    def _paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = ...) -> None:
        rect = QRectF(self.actor.actor_dot.bounding_rect)

        logicshape_comp = self.actor.getComponent("CLogicShapeComponent")
        if not logicshape_comp.pLogicShape:
            if rect != self.bounding_rect:
                self.prepareGeometryChange()
                self.bounding_rect = rect

            return

        vPos = vector2f(self.actor.level_data.vPos) + vector2f(logicshape_comp.pLogicShape.vPos)
        ls_type = logicshape_comp.pLogicShape["@type"]

        if ls_type == "game::logic::collision::CPolygonCollectionShape":
            rect = QRectF()
            for poly in logicshape_comp.pLogicShape.oPolyCollection.vPolys:
                qpoly = QPolygonF()
                for segment in poly.oSegmentData:
                    qpoly.append(vPos + vector2f(segment.vPos))

                if poly.bClosed:
                    qpoly.append(qpoly.first())
                    painter.drawPolygon(qpoly)
                else:
                    painter.drawPolyline(qpoly)

                rect = rect.united(qpoly.boundingRect())

        elif ls_type == "game::logic::collision::CAABoxShape2D":
            p1 = vPos + vector2f(logicshape_comp.pLogicShape.v2Min)
            p2 = vPos + vector2f(logicshape_comp.pLogicShape.v2Max)
            rect = QRectF(p1, p2)
            painter.drawRect(rect)
        elif ls_type == "game::logic::collision::COBoxShape2D":
            halfExtent = vector2f(logicshape_comp.pLogicShape.v2Extent) / 2
            rads = radians(logicshape_comp.pLogicShape.fDegrees)

            # do a simple rect draw if aligned
            if rads == 0:
                rect = QRectF(vPos - halfExtent, vPos + halfExtent)
                painter.drawRect(rect)
            else:
                # cache some values for rotations
                s = sin(rads)
                c = cos(rads)
                xs = s * halfExtent.x()
                xc = c * halfExtent.x()
                ys = s * halfExtent.y()
                yc = c * halfExtent.y()

                self.actor.logger.warning(
                    "A COBoxShape2D actually has a rotation value! Make sure %s/%s/%s is rendered correctly",
                    self.actor.ref.layer,
                    self.actor.ref.sublayer,
                    self.actor.ref.name,
                )
                poly = QPolygonF()
                topleft = QPointF(-xc + ys, -xs - yc)
                topright = QPointF(-xc - ys, -xs + yc)
                bottomright = QPointF(xc - ys, xs + yc)
                bottomleft = QPointF(xc + ys, xs - yc)
                poly.append(topleft)
                poly.append(topright)
                poly.append(bottomright)
                poly.append(bottomleft)
                poly.append(topleft)
                rect = poly.boundingRect()
                painter.drawPolygon(poly)

        else:
            self.actor.logger.warning(
                "Poly with type %s detected! %s/%s/%s",
                ls_type,
                self.actor.ref.layer,
                self.actor.ref.sublayer,
                self.actor.ref.name,
            )

        if rect != self.bounding_rect:
            self.prepareGeometryChange()
            self.bounding_rect = rect
