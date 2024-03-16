from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QStyleOptionGraphicsItem, QWidget
from PyQt5.QtCore import QRectF

from dreaditor.actor import Actor
from dreaditor.painters.collision import paint_all_collision, paint_door, paint_tiles
from dreaditor.painters.logicpath import paint_logicpath
from dreaditor.painters.logicshape import paint_logicshape
from dreaditor.painters.worldgraph import paint_worldgraph


def detailed_actor_paint(actor: Actor, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None) -> QRectF:
    rect = QRectF()
    if actor.getComponent("CDoorLifeComponent") or actor.getComponent("CDoorEmmyFXComponent") or actor.getComponent("CDoorCentralUnitLifeComponent"):
        rect = rect.united(paint_door(actor, painter, option, widget))
    elif actor.bmscc:
        rect = rect.united(paint_all_collision(actor, painter, option, widget))
    elif actor.getComponent("CBreakableTileGroupComponent"):
        rect = rect.united(paint_tiles(actor, painter, option, widget))
    elif actor.getComponent("CWorldGraph"):
        rect = rect.united(paint_worldgraph(actor, painter, option, widget))
    return rect

def selected_actor_paint(actor: Actor, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None) -> QRectF:
    rect = QRectF()

    if actor.getComponent("CLogicShapeComponent"):
        rect = rect.united(paint_logicshape(actor, painter, option, widget))
    elif actor.getComponent("CLogicPathComponent"):
        rect = rect.united(paint_logicpath(actor, painter, option, widget))
    return rect
