from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import QBrush, QColor, QPainter, QPainterPath, QPen, QPolygonF
from PySide6.QtWidgets import QStyleOptionGraphicsItem, QWidget

from dreaditor.painters.base_painter import BasePainterWidget

if TYPE_CHECKING:
    from PySide6.QtWidgets import QStyleOptionGraphicsItem, QWidget

LOGGER = logging.getLogger(__name__)


def aabox2d_to_rect(aabox2d: dict, vPos: QPointF) -> QRectF:
    halfw = aabox2d["data"]["size"][0] / 2
    halfh = aabox2d["data"]["size"][1] / 2
    p1 = vPos + QPointF(aabox2d["data"]["position"][0] - halfw, halfh - aabox2d["data"]["position"][1])
    p2 = vPos + QPointF(aabox2d["data"]["position"][0] + halfw, -halfh - aabox2d["data"]["position"][1])
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


class CollisionDataFileWidget(BasePainterWidget):
    config_val = "paintCollision"

    def _paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = ...) -> None:
        rect = QRectF()
        vPos = QPointF(self.actor.level_data.vPos[0], -self.actor.level_data.vPos[1])

        for layer in self.actor.bmscc.raw.layers:
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

        if rect != self.bounding_rect:
            self.prepareGeometryChange()
            self.bounding_rect = rect


class BmsadCollisionWidget(BasePainterWidget):
    config_val = "paintCollision"

    def _paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = ...) -> None:
        rect = QRectF()
        vPos = QPointF(self.actor.level_data.vPos[0], -self.actor.level_data.vPos[1])

        for func in self.actor.bmsad.components["COLLISION"].functions:
            if func.name == "CreateCollider":
                if func.get_param(5) == "AABOX2D":
                    entry = {
                        "data": {
                            "position": [
                                func.get_param(6),
                                func.get_param(7),
                                func.get_param(8),
                            ],
                            "size": [func.get_param(9), func.get_param(10)],
                        }
                    }
                    r = aabox2d_to_rect(entry, vPos)
                    painter.drawRect(r)
                    rect = rect.united(r)
                else:
                    LOGGER.warning(
                        "Unknown collider type in BMSAD for actor (%s/%s/%s): %s",
                        self.actor.ref.layer,
                        self.actor.ref.sublayer,
                        self.actor.ref.name,
                        func.get_param(5),
                    )

        if rect != self.bounding_rect:
            self.prepareGeometryChange()
            self.bounding_rect = rect


class DoorPainterWidget(BasePainterWidget):
    DOOR_PEN = QPen(QColor(0, 0, 0, 255), 10)
    ADDITIONAL_COLLIDER_PEN = QPen(QColor(64, 0, 255, 32), 10)
    config_val = "paintDoors"

    def _paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = ...) -> None:
        vPos = QPointF(self.actor.level_data.vPos[0], -self.actor.level_data.vPos[1])
        door_type: str = self.actor.level_data.oActorDefLink.split("/")[2]
        entry_name = door_type if door_type in ["doorframe", "tunnelframe"] else "door"

        col_layer = [layer for layer in self.actor.bmscc.raw.layers if layer.name == "collision_layer"][0]
        aabox = [entry for entry in col_layer.entries if entry.name == entry_name][0]
        rect = aabox2d_to_rect(aabox, vPos)

        painter.setPen(self.DOOR_PEN)
        painter.setBrush(QBrush(QColor(255, 255, 255, 128)))
        painter.drawRect(rect)

        # add sensor box if it's a presence door
        if "presence" in door_type:
            sensor_aabox = [entry for entry in col_layer.entries if entry.name == "sensor"][0]
            sensor_rect = aabox2d_to_rect(sensor_aabox, vPos)
            painter.setBrush(QBrush(QColor(0, 0, 0, 0)))
            painter.setPen(self.ADDITIONAL_COLLIDER_PEN)
            painter.drawRect(sensor_rect)

        if rect != self.bounding_rect:
            self.prepareGeometryChange()
            self.bounding_rect = rect


class ShieldPainterWidget(BasePainterWidget):
    SHIELD_COLORS = {
        "doorwidebeam": QColor(255, 255, 0, 128),
        "door_shield_plasma": QColor(137, 243, 54, 128),
        "doorwavebeam": QColor(255, 0, 255, 128),
        "shield_diffusion": QColor(255, 0, 0, 128),
        "doorshieldmissile": QColor(255, 128, 0, 128),
        "doorshieldsupermissile": QColor(0, 255, 0, 128),
        "shield_icemissile": QColor(0, 255, 255, 128),
        "shield_storm_mssl": QColor(255, 128, 0, 128),
        "shield_bombs_regular__": QColor(255, 0, 150, 128),
        "shield_cross_bomb_____": QColor(255, 0, 125, 128),
        "doorshieldpowerbomb___": QColor(255, 96, 0, 128),
    }

    config_val = "paintDoors"

    def _paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = ...) -> None:
        vPos = QPointF(self.actor.level_data.vPos[0], -self.actor.level_data.vPos[1])
        side = "collision_L" if self.actor.level_data.vAng[1] < 0 else "collision_R"
        shield_type: str = self.actor.level_data.oActorDefLink.split("/")[2]

        col_layer = [layer for layer in self.actor.bmscc.raw.layers if layer.name == "collision_layer"][0]
        aabox = [entry for entry in col_layer.entries if entry.name == side][0]
        polys = polycollection_to_polys(aabox, vPos)

        painter.setPen(QPen(self.SHIELD_COLORS[shield_type], 10))
        painter.setBrush(QBrush(self.SHIELD_COLORS[shield_type]))
        painter.brush().color().setAlpha(48)
        bbox = QRectF()
        for p in polys:
            painter.drawPolygon(p)
            bbox = bbox.united(p.boundingRect())

        if polys != self.bounding_rect:
            self.prepareGeometryChange()
            self.bounding_rect = bbox


class TilegroupPainterWidget(BasePainterWidget):
    config_val = "paintBreakables"

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

    def _paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget | None = ...) -> None:
        vPos = QPointF(self.actor.level_data.vPos[0], -self.actor.level_data.vPos[1])
        tile_comp = self.actor.getComponent("CBreakableTileGroupComponent")
        rect = QRectF()
        painter.setPen(QPen(QColor(0, 0, 0), 1))

        for tile in tile_comp.aGridTiles:
            tile_rect = QRectF(
                vPos + QPointF(100.0 * tile.vGridCoords[0], -100.0 * (tile.vGridCoords[1] + 1)),
                vPos + QPointF(100.0 * (tile.vGridCoords[0] + 1), -100.0 * tile.vGridCoords[1]),
            )
            painter.setBrush(self.TILE_BRUSHES[tile.eTileType])
            painter.drawRect(tile_rect)
            rect = rect.united(tile_rect)

        if rect != self.bounding_rect:
            self.prepareGeometryChange()
            self.bounding_rect = rect

    def shape(self) -> QPainterPath:
        res = QPainterPath()
        vPos = QPointF(self.actor.level_data.vPos[0], -self.actor.level_data.vPos[1])
        tile_comp = self.actor.getComponent("CBreakableTileGroupComponent")

        for tile in tile_comp.aGridTiles:
            res.addRect(
                QRectF(
                    vPos + QPointF(100.0 * tile.vGridCoords[0], -100.0 * (tile.vGridCoords[1] + 1)),
                    vPos + QPointF(100.0 * (tile.vGridCoords[0] + 1), -100.0 * tile.vGridCoords[1]),
                )
            )

        return res
