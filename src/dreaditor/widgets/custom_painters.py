from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QPolygonF
from PyQt5.QtWidgets import QStyleOptionGraphicsItem, QWidget
from PyQt5.QtCore import QRectF, QPointF

from mercury_engine_data_structures.formats.bmscc import Bmscc

from dreaditor.actor import Actor

def detailed_actor_paint(actor: Actor, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None) -> QRectF:
    rect = QRectF()
    if actor.getComponent("CDoorLifeComponent"):
        rect = rect.united(paint_door(actor, painter, option, widget))
    if actor.getComponent("CCollisionComponent") and actor.bmsad:
        rect = rect.united(paint_collision(actor, painter, option, widget))
    return rect


DOOR_PEN = QPen(QColor(255, 255, 255, 255), 20)
def paint_door(actor: Actor, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None) -> QRectF:
    door_type = actor.level_data.oActorDefLink.split('/')[2]
    rect = QRectF(QPointF(actor.level_data.vPos[0] - 150, -actor.level_data.vPos[1]), QPointF(actor.level_data.vPos[0] + 150, -actor.level_data.vPos[1] - 300))
    if door_type == "doorshutter":
        # convert door to half-width and +100 height
        rect.adjust(75, 0, -75, -100)
    painter.setPen(DOOR_PEN)
    painter.pen().setWidth(50)
    painter.setBrush(QColor(255, 255, 0, 255))
    painter.drawRect(rect)
    return rect

COLLIDER_PEN_UNSELECTED = QPen(QColor(255, 0, 0, 128), 15)
COLLIDER_PEN_SELECTED = QPen(QColor(255, 0, 255, 128), 20)
COLLIDER_BRUSH = QBrush(QColor(0, 0, 0, 0))
def paint_collision(actor: Actor, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None) -> QRectF:
    
    coll_dep = actor.bmsad.components["COLLISION"].dependencies
    coll_fp = coll_dep.file

    rect = QRectF()

    painter.setBrush(COLLIDER_BRUSH)
    painter.setPen(COLLIDER_PEN_SELECTED if actor.isSelected else COLLIDER_PEN_UNSELECTED)
    vPos = QPointF(actor.level_data.vPos[0], -actor.level_data.vPos[1])

    if isinstance(coll_fp, str) and coll_fp != "Unassigned":
        bmscd = actor.editor.get_parsed_asset(coll_fp.replace("\\", "/"), type_hint=Bmscc)
        
        for layer in bmscd.raw.layers:
            for entry in layer.entries:
                if entry.type == u'AABOX2D':
                    halfw = entry.data.size[0] / 2
                    halfh = entry.data.size[1] / 2
                    p1 = vPos + QPointF(entry.data.center[0] - halfw, halfh - entry.data.center[1])
                    p2 = vPos + QPointF(entry.data.center[0] +  halfw, - halfh - entry.data.center[1])
                    r = QRectF(p1, p2)
                    painter.drawRect(r)
                    rect = rect.united(r)

                elif entry.type == u'POLYCOLLECTION2D':
                    for polygon in entry.data.polys:
                        if polygon.num_points == 0:
                            continue

                        poly = QPolygonF()
                        for p in polygon.points:
                            poly.append(vPos + QPointF(p.x, -p.y))
                        if polygon.loop:
                            poly.append(poly.first())
                        
                        rect = rect.united(poly.boundingRect())
                        painter.drawPolyline(poly)
    
    return rect
                    