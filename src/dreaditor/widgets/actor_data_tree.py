from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget

from dreaditor.actor import Actor, ActorSelectionState
from dreaditor.actor_reference import ActorRef
from dreaditor.widgets.actor_data_tree_item import ActorDataTreeItem

if TYPE_CHECKING:
    from dreaditor.rom_manager import RomManager


class ActorDataTreeWidget(QTreeWidget):
    rom_manager: RomManager

    def __init__(self, rom_manager: RomManager, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.logger = logging.getLogger(type(self).__name__)
        self.rom_manager = rom_manager

        self.setHeaderLabels(["name", "value"])
        self.setColumnCount(2)
        self.itemDoubleClicked.connect(self.onItemDoubleClicked)

    def LoadActor(self, actor: Actor):
        # guard against loading actor multiple times
        idx = self.FindActor(actor)
        if idx is not None:
            return

        top_actor = ActorDataTreeItem(actor)
        cc_data = QTreeWidgetItem(["Collision Cameras"])
        for subarea_id, cc_names in actor.subarea_setups.items():
            subarea_widget = QTreeWidgetItem([subarea_id])
            subarea_widget.addChildren([QTreeWidgetItem(["", cc]) for cc in cc_names])
            cc_data.addChild(subarea_widget)
        top_actor.addChild(cc_data)

        # load the level data from the brfld
        level_data = QTreeWidgetItem(["Level Data"])
        self.AddKeysToActor(level_data, actor.level_data)
        top_actor.addChild(level_data)

        # load the bmsad components, actionsets, soundfx
        if actor.bmsad is not None:
            bmsad = actor.bmsad
            bmsad_data = QTreeWidgetItem(["Actordef Data"])
            bmsad_comps = QTreeWidgetItem(["Components"])
            self.AddKeysToActor(bmsad_comps, bmsad.raw.components)
            bmsad_actionsets = QTreeWidgetItem(["Action Sets"])
            bmsad_actionsets.addChildren([QTreeWidgetItem(["", item]) for item in bmsad.raw.action_sets])
            bmsad_soundfx = QTreeWidgetItem(["Sound FX"])
            bmsad_soundfx.addChildren(
                [QTreeWidgetItem(["", f"{item[0]} (VOL {item[1]})"]) for item in bmsad.raw.sound_fx]
            )
            bmsad_data.addChildren([bmsad_comps, bmsad_actionsets, bmsad_soundfx])
            top_actor.addChild(bmsad_data)
        else:
            self.logger.warning(
                "The BMSAD for actor %s/%s/%s cannot be accessed due to a bug in mercury-engine-data-structures",
                actor.ref.layer,
                actor.ref.sublayer,
                actor.ref.name,
            )

        if actor.bmscc is not None:
            bmscc_item = QTreeWidgetItem(["BMSCC"])
            self.AddKeysToActor(bmscc_item, actor.bmscc.raw)
            top_actor.addChild(bmscc_item)

        # add top actor, expand recursively but make the root item unexpanded
        self.addTopLevelItem(top_actor)
        self.expandRecursively(self.indexFromItem(top_actor))
        top_actor.setExpanded(False)

    def FindActor(self, actor: Actor) -> int:
        # find actor in top-level elements
        for actor_idx in range(self.topLevelItemCount()):
            if self.topLevelItem(actor_idx).actor.ref == actor.ref:
                return actor_idx

        return None

    def UnloadActor(self, actor: Actor):
        # find actor in top-level elements
        idx = self.FindActor(actor)

        if idx is None:
            self.logger.info(
                "Tried to unload actor %s/%s/%s from data tree, but could not be found!",
                actor.ref.layer,
                actor.ref.sublayer,
                actor.ref.name,
            )
            return

        self.takeTopLevelItem(idx)

    def AddKeysToActor(self, item: QTreeWidgetItem, val: dict):
        for k, v in val.items():
            if k in ["_io"]:
                continue

            if isinstance(v, dict):
                child = QTreeWidgetItem([k, ""])
                self.AddKeysToActor(child, v)
                item.addChild(child)

            elif isinstance(v, list):
                child = QTreeWidgetItem([k, ""])

                if len(v) > 0 and len(v) <= 4 and isinstance(v[0], int | float):
                    res = "["
                    for va in v:
                        res += f"{va:.3f}"
                        res += ", "
                    res = res[:-2] + "]"
                    item.addChild(QTreeWidgetItem([k, res]))
                else:
                    self.AddKeysToActor(child, {str(i): value for i, value in enumerate(v)})
                    item.addChild(child)

            else:
                item.addChild(QTreeWidgetItem([k, str(v)]))

    @Slot(QTreeWidgetItem, int)
    def onItemDoubleClicked(self, item: QTreeWidgetItem, col):
        if isinstance(item, ActorDataTreeItem):
            item.actor.OnSelected(ActorSelectionState.Unselected)
        else:
            # attempt to decode actor link
            val = item.text(1)
            if val.startswith("Root:") and val.count(":") > 5:
                elements = val.split(":")
                if (
                    elements[0] == "Root"
                    and elements[1] == "pScenario"
                    and elements[3] == "dctSublayers"
                    and elements[5] == "dctActors"
                ):
                    self.logger.info("Opening actor from link: %s/%s/%s", elements[2], elements[4], elements[6])
                    # select actor
                    ref = ActorRef(self.rom_manager.scenario, elements[2], elements[4], elements[6])
                    actor = self.rom_manager.get_actor_from_ref(ref)
                    actor.OnSelected(ActorSelectionState.Selected)
            elif (
                item.parent() is not None
                and item.parent().parent() is not None
                and item.parent().parent().text(0) == "Collision Cameras"
            ):
                setup_id = item.parent().text(0)
                cc_id = item.text(1)

                self.rom_manager.main_window.subareas_list_tree.select_camera(setup_id, cc_id)
