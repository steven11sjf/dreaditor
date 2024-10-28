from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QTreeWidgetItem

if TYPE_CHECKING:
    from dreaditor.actor import Actor


class ActorDataTreeItem(QTreeWidgetItem):
    actor: Actor

    def __init__(self, actor: Actor) -> None:
        super().__init__([actor.ref.name])
        self.actor = actor
