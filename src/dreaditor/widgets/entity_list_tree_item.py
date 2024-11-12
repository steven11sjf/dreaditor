from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QTreeWidgetItem

if TYPE_CHECKING:
    from dreaditor.actor import Actor
    from dreaditor.actor_reference import ActorRef


NORMAL_BACKGROUND = QColor(0x333333)
HIGHLIGHTED_BACKGROUND = QColor(0x666666)


class EntityListTreeWidgetItem(QTreeWidgetItem):
    actor: Actor
    reference: ActorRef

    def __init__(self, actor: Actor) -> None:
        super().__init__([actor.level_data.sName])

        self.actor = actor
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
        self.setCheckState(0, Qt.CheckState.Checked)
        actor.entity_list_items.append(self)

    def set_hovered(self, val: bool):
        self.setBackground(0, HIGHLIGHTED_BACKGROUND if val else NORMAL_BACKGROUND)

    def set_selected(self, val: bool):
        font = self.font(0)
        font.setBold(val)
        self.setFont(0, font)
