import logging

from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QFont

from dreaditor.actor_reference import ActorRef
from dreaditor.constants import Scenario
from dreaditor.rom_manager import RomManager


ACTORDEF_FONT = QFont().setBold(True)

class ActorDataTreeWidget(QTreeWidget):
    rom_manager: RomManager | None
    brfld_node: QTreeWidgetItem

    def __init__(self, rom_manager: RomManager, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.logger = logging.getLogger(type(self).__name__)
        self.setHeaderLabels(["name", "value"])
        self.setColumnCount(2)


        self.rom_manager = rom_manager

    def LoadActor(self, ref: ActorRef):
        actor = self.rom_manager.GetActorFromRef(ref)

        if actor is None:
            self.logger.info("Could not find actor %s/%s/%s", ref.layer, ref.sublayer, ref.name)
            return
        
        self.clear()

        # load the level data from the brfld
        top_actor = QTreeWidgetItem([actor.sName])
        level_data = QTreeWidgetItem(["Level Data"])
        self.AddKeysToActor(level_data, actor)

        # load the bmsad components, actionsets, soundfx
        bmsad = self.rom_manager.GetActorDef(actor.oActorDefLink)
        bmsad_data = QTreeWidgetItem(["Actordef Data"])
        bmsad_comps = QTreeWidgetItem(["Components"])
        self.AddKeysToActor(bmsad_comps, bmsad.raw.components)
        bmsad_actionsets = QTreeWidgetItem(["Action Sets"])
        bmsad_actionsets.addChildren([QTreeWidgetItem(["", item]) for item in bmsad.raw.action_sets])
        bmsad_soundfx = QTreeWidgetItem(["Sound FX"])
        bmsad_soundfx.addChildren([QTreeWidgetItem(["", f"{item[0]} (VOL {item[1]})"]) for item in bmsad.raw.sound_fx])
        bmsad_data.addChildren([bmsad_comps, bmsad_actionsets, bmsad_soundfx])

        top_actor.addChildren([level_data, bmsad_data])
        self.addTopLevelItem(top_actor)
        self.expandAll()
        
    def AddKeysToActor(self, item: QTreeWidgetItem, val: dict):
        for k,v in val.items():
            if isinstance(v, dict):
                child = QTreeWidgetItem([k, ""])
                self.AddKeysToActor(child, v)
                item.addChild(child)
            
            elif isinstance(v, list):
                child = QTreeWidgetItem([k, ""])

                if len(v) > 0 and len(v) <= 4 and isinstance(v[0], int | float):
                    res = "["
                    for va in v:
                        res += str(va)
                        res += ", "
                    res = res[:-2] + "]"
                    item.addChild(QTreeWidgetItem([k, res]))
                else:
                    self.AddKeysToActor(child, { str(i): value for i, value in enumerate(v)})
                    item.addChild(child)
            
            else:
                item.addChild(QTreeWidgetItem([k, str(v)]))
