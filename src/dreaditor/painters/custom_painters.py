from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QStyleOptionGraphicsItem, QWidget
from PySide6.QtCore import QRectF

from dreaditor.actor import Actor
from dreaditor.painters.collision import paint_all_collision, paint_door, paint_tiles
from dreaditor.painters.logicpath import paint_logicpath
from dreaditor.painters.logicshape import paint_logicshape
from dreaditor.painters.worldgraph import paint_worldgraph
from dreaditor.config import get_config_data


def custom_painters(actor: Actor, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget |  None) -> QRectF:
    rect = QRectF()

    if actor.getComponent("CDoorLifeComponent") or actor.getComponent("CDoorEmmyFXComponent") or actor.getComponent("CDoorCentralUnitLifeComponent"):
        if actor.isSelected or get_config_data("paintDoors"):
            rect = rect.united(paint_door(actor, painter, option, widget))
    elif actor.bmscc:
        if actor.isSelected or get_config_data("paintCollision"):
            rect = rect.united(paint_all_collision(actor, painter, option, widget))

    if actor.getComponent("CBreakableTileGroupComponent"):
        if actor.isSelected or get_config_data("paintBreakables"):
            rect = rect.united(paint_tiles(actor, painter, option, widget))

    if actor.getComponent("CLogicShapeComponent"):
        if actor.isSelected or get_config_data("paintLogicShapes"):
            rect = rect.united(paint_logicshape(actor, painter, option, widget))
    
    if actor.getComponent("CLogicPathComponent"):
        if actor.isSelected or get_config_data("paintLogicPaths"):
            rect = rect.united(paint_logicpath(actor, painter, option, widget))
    
    if actor.getComponent("CWorldGraph"):
        if actor.isSelected or get_config_data("paintWorldGraph"):
            rect = rect.united(paint_worldgraph(actor, painter, option, widget))

    return rect
