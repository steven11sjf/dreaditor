from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import QBrush, QColor, QPainter, QPen, QPolygonF

if TYPE_CHECKING:
    from PySide6.QtWidgets import QStyleOptionGraphicsItem, QWidget

    from dreaditor.actor import Actor

COLLIDER_PEN_UNSELECTED = QPen(QColor(255, 0, 0, 128), 15)
COLLIDER_PEN_SELECTED = QPen(QColor(255, 0, 255, 128), 20)
COLLIDER_BRUSH = QBrush(QColor(0, 0, 0, 0))


def aabox2d_to_rect(aabox2d: dict, vPos: QPointF) -> QRectF:
    halfw = aabox2d.data.size[0] / 2
    halfh = aabox2d.data.size[1] / 2
    p1 = vPos + QPointF(aabox2d.data.position[0] - halfw, halfh - aabox2d.data.position[1])
    p2 = vPos + QPointF(aabox2d.data.position[0] + halfw, -halfh - aabox2d.data.position[1])
    return QRectF(p1, p2)


def polycollection_to_polys(polycollection: dict, vPos: QPointF) -> list[QPolygonF]:
    res = []
    poly_pos = vPos + QPointF(polycollection.data.position[0], -polycollection.data.position[1])
    for polygon in polycollection.data.polys:
        if polygon.num_points == 0:
            continue

        poly = QPolygonF()
        for p in polygon.points:
            poly.append(poly_pos + QPointF(p.x, -p.y))
        if polygon.loop:
            poly.append(poly.first())

        res.append(poly)

    return res


def paint_all_collision(
    actor: Actor, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None
) -> QRectF:
    rect = QRectF()

    painter.setBrush(COLLIDER_BRUSH)
    painter.setPen(COLLIDER_PEN_SELECTED if actor.isSelected else COLLIDER_PEN_UNSELECTED)
    vPos = QPointF(actor.level_data.vPos[0], -actor.level_data.vPos[1])

    for layer in actor.bmscc.raw.layers:
        for entry in layer.entries:
            if entry.type == "AABOX2D":
                r = aabox2d_to_rect(entry, vPos)
                painter.drawRect(r)
                rect = rect.united(r)

            elif entry.type == "POLYCOLLECTION2D":
                polys = polycollection_to_polys(entry, vPos)
                for p in polys:
                    painter.drawPolyline(p)
                    rect = rect.united(p.boundingRect())

            elif entry.type == "CIRCLE":
                center = vPos + QPointF(entry.data.position[0], -entry.data.position[1])
                size = entry.data.size
                topLeft = center - QPointF(size, -size)
                bottomRight = center + QPointF(size, -size)
                circle_rect = QRectF(topLeft, bottomRight)

                painter.drawEllipse(circle_rect)
                rect = rect.united(circle_rect)

    return rect


DOOR_PEN = QPen(QColor(0, 0, 0, 255), 10)


def paint_door(
    actor: Actor, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None
) -> QRectF:
    vPos = QPointF(actor.level_data.vPos[0], -actor.level_data.vPos[1])
    door_type: str = actor.level_data.oActorDefLink.split("/")[2]
    entry_name = door_type if door_type in ["doorframe", "tunnelframe"] else "door"

    col_layer = [layer for layer in actor.bmscc.raw.layers if layer.name == "collision_layer"][0]
    aabox = [entry for entry in col_layer.entries if entry.name == entry_name][0]
    rect = aabox2d_to_rect(aabox, vPos)

    painter.setPen(DOOR_PEN)
    painter.setBrush(QBrush(QColor(255, 255, 255, 128)))
    painter.drawRect(rect)

    # add sensor box if it's a presence door
    if "presence" in door_type:
        sensor_aabox = [entry for entry in col_layer.entries if entry.name == "sensor"][0]
        sensor_rect = aabox2d_to_rect(sensor_aabox, vPos)
        painter.setBrush(QBrush(QColor(0, 0, 0, 0)))
        painter.setPen(QPen(QColor(64, 0, 255, 32), 10))
        painter.drawRect(sensor_rect)
    return rect


TILE_BRUSHES: dict[int, QBrush] = {
    1: QBrush(QColor(255, 255, 255, 128)),  # powerbeam
    2: QBrush(QColor(255, 0, 255, 128)),  # bomb
    3: QBrush(QColor(255, 0, 0, 128)),  # missile
    4: QBrush(QColor(0, 255, 0, 128)),  # super missile
    5: QBrush(QColor(255, 165, 0, 128)),  # powerbomb
    6: QBrush(QColor(0, 0, 255, 128)),  # screw attack
    7: QBrush(QColor(128, 128, 128, 128)),  # weight
    8: QBrush(QColor(195, 195, 190, 128)),  # baby hatchling
    9: QBrush(QColor(255, 255, 0, 128)),  # speedboost
}


def paint_tiles(
    actor: Actor, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None
) -> QRectF:
    vPos = QPointF(actor.level_data.vPos[0], -actor.level_data.vPos[1])
    tile_comp = actor.getComponent("CBreakableTileGroupComponent")
    brect = QRectF()
    for tile in tile_comp.aGridTiles:
        rect = QRectF(
            vPos + QPointF(100.0 * tile.vGridCoords[0], -100.0 * (tile.vGridCoords[1] + 1)),
            vPos + QPointF(100.0 * (tile.vGridCoords[0] + 1), -100.0 * tile.vGridCoords[1]),
        )
        painter.setBrush(TILE_BRUSHES[tile.eTileType])
        painter.drawRect(rect)
        brect = brect.united(rect)

    return brect
