from __future__ import annotations

import logging
from math import cos, radians, sin
from typing import TYPE_CHECKING

from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import QBrush, QColor, QPainter, QPen, QPolygonF

if TYPE_CHECKING:
    from PySide6.QtWidgets import QStyleOptionGraphicsItem, QWidget

    from dreaditor.actor import Actor

LOGGER = logging.getLogger(__name__)


def paint_logicshape(
    actor: Actor, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None
) -> QRectF:
    rect = QRectF()

    painter.setBrush(QBrush(QColor(255, 255, 64, 8)))
    painter.setPen(QPen(QColor(255, 255, 64, 128), 15))
    logicshape_comp = actor.getComponent("CLogicShapeComponent")
    if logicshape_comp.pLogicShape is None:
        return rect

    vPos = QPointF(
        actor.level_data.vPos[0] + logicshape_comp.pLogicShape.vPos[0],
        -actor.level_data.vPos[1] - logicshape_comp.pLogicShape.vPos[1],
    )
    ls_type = logicshape_comp.pLogicShape["@type"]

    if ls_type == "game::logic::collision::CPolygonCollectionShape":
        for poly in logicshape_comp.pLogicShape.oPolyCollection.vPolys:
            qpoly = QPolygonF()
            for segment in poly.oSegmentData:
                qpoly.append(vPos + QPointF(segment.vPos[0], -segment.vPos[1]))

            if poly.bClosed:
                qpoly.append(qpoly.first())

            painter.drawPolygon(qpoly)
            rect = rect.united(qpoly.boundingRect())
    elif ls_type == "game::logic::collision::CAABoxShape2D":
        p1 = vPos + QPointF(logicshape_comp.pLogicShape.v2Min[0], -logicshape_comp.pLogicShape.v2Min[1])
        p2 = vPos + QPointF(logicshape_comp.pLogicShape.v2Max[0], -logicshape_comp.pLogicShape.v2Max[1])
        rect = QRectF(p1, p2)
        painter.drawRect(rect)
    elif ls_type == "game::logic::collision::COBoxShape2D":
        halfExtent = QPointF(logicshape_comp.pLogicShape.v2Extent[0] / 2, -logicshape_comp.pLogicShape.v2Extent[1] / 2)
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

            actor.logger.warning(
                "A COBoxShape2D actually has a rotation value! Make sure %s/%s/%s is rendered correctly",
                actor.ref.layer,
                actor.ref.sublayer,
                actor.ref.name,
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
        LOGGER.warning(f"Poly with type {ls_type} detected! {actor.ref.layer}/{actor.ref.sublayer}/{actor.ref.name}")

    return rect
