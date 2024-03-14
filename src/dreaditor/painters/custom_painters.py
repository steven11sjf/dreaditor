from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QStyleOptionGraphicsItem, QWidget
from PyQt5.QtCore import QRectF

from dreaditor.actor import Actor
from dreaditor.painters.collision import paint_all_collision, paint_door, paint_tiles
from dreaditor.painters.worldgraph import paint_worldgraph


def detailed_actor_paint(actor: Actor, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None) -> QRectF:
    rect = QRectF()
    if actor.getComponent("CDoorLifeComponent") or actor.getComponent("CDoorEmmyFXComponent"):
        rect = rect.united(paint_door(actor, painter, option, widget))
    elif actor.bmscc:
        rect = rect.united(paint_all_collision(actor, painter, option, widget))
    elif actor.getComponent("CBreakableTileGroupComponent"):
        rect = rect.united(paint_tiles(actor, painter, option, widget))
    elif actor.getComponent("CWorldGraph"):
        rect = rect.united(paint_worldgraph(actor, painter, option, widget))
    return rect
