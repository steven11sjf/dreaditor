from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeWidgetItem

if TYPE_CHECKING:
    from dreaditor.actor import Actor
    from dreaditor.actor_reference import ActorRef


class EntityListTreeWidgetItem(QTreeWidgetItem):
    actor: Actor
    reference: ActorRef

    def __init__(self, actor: Actor) -> None:
        super().__init__([actor.level_data.sName])

        self.actor = actor
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
        self.setCheckState(0, Qt.CheckState.Checked)
        actor.entity_list_items.append(self)
