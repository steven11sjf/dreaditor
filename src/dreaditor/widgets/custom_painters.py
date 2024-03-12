from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtWidgets import QStyleOptionGraphicsItem, QWidget
from PyQt5.QtCore import QRectF, QPointF

from dreaditor.actor import Actor

def detailed_actor_paint(actor: Actor, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None):
    if actor.getComponent("CDoorLifeComponent"):
        paint_door(actor, painter, option, widget)


DOOR_PEN = QPen(QColor(255, 255, 255, 255), 20)
def paint_door(actor: Actor, painter: QPainter | None, option: QStyleOptionGraphicsItem | None, widget: QWidget | None):
    door_type = actor.level_data.oActorDefLink.split('/')[2]
    rect = QRectF(QPointF(actor.level_data.vPos[0] - 150, -actor.level_data.vPos[1]), QPointF(actor.level_data.vPos[0] + 150, -actor.level_data.vPos[1] - 300))
    if door_type == "doorshutter":
        # convert door to half-width and +100 height
        rect.adjust(75, 0, -75, -100)
    painter.setPen(DOOR_PEN)
    painter.pen().setWidth(50)
    painter.setBrush(QColor(255, 255, 0, 255))
    painter.drawRect(rect)
