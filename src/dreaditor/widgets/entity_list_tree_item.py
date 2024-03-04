from PyQt5.QtWidgets import QTreeWidgetItem, QWidget
from PyQt5.QtCore import Qt

from dreaditor.actor_reference import ActorRef
from dreaditor.constants import Scenario
from dreaditor.rom_manager import RomManager


class EntityListTreeWidgetItem(QTreeWidgetItem):
    rom_manager: RomManager | None
    data: dict
    reference: ActorRef

    def __init__(self, rom_manager: RomManager, data: dict, ref: ActorRef, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        
        self.rom_manager = rom_manager
        self.data = data
        self.reference = ref
