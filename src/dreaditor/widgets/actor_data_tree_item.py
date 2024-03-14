import logging

from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget

from dreaditor.actor import Actor

class ActorDataTreeItem(QTreeWidgetItem):
    actor: Actor

    def __init__(self, actor: Actor) -> None:
        super().__init__([actor.ref.name])
        self.actor = actor
    
    