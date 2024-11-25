from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

from mercury_engine_data_structures.file_tree_editor import FileTreeEditor
from mercury_engine_data_structures.formats.bmmap import Bmmap
from mercury_engine_data_structures.formats.bmsad import Bmsad
from mercury_engine_data_structures.formats.bmscc import Bmscc
from mercury_engine_data_structures.formats.bmsnav import Bmsnav
from mercury_engine_data_structures.formats.brfld import ActorLayer, Brfld
from mercury_engine_data_structures.formats.brsa import Brsa
from mercury_engine_data_structures.game_check import Game
from mercury_engine_data_structures.romfs import ExtractedRomFs
from PySide6.QtCore import Qt

from dreaditor.actor import Actor
from dreaditor.actor_reference import ActorRef
from dreaditor.config import CurrentConfiguration

if TYPE_CHECKING:
    from dreaditor.constants import Scenario
    from dreaditor.main_window import DreaditorWindow
    from dreaditor.widgets.collision_camera_item import CollisionCameraItem


class RomManager:
    main_window: DreaditorWindow
    editor: FileTreeEditor | None
    path: str | None

    isScenarioLoaded: bool = False
    scenario: Scenario | None
    actors: list[Actor]
    brfld: Brfld | None

    def __init__(self, main_window: DreaditorWindow):
        self.logger = logging.getLogger(type(self).__name__)
        self.main_window = main_window
        self.editor = None
        self.path = CurrentConfiguration["romfs_dir"]
        self.logger.info("Path loaded from config: %s", self.path)
        self.actors = []
        self.select_rom(self.path)

    def select_rom(self, path: str):
        if path is None:
            return

        self.path = path
        try:
            self.editor = FileTreeEditor(ExtractedRomFs(Path(path)), target_game=Game.DREAD)
            self.logger.info(f"Selected RomFS at {path} with version {self.editor.version}")
            CurrentConfiguration["romfs_dir"] = path
        except ValueError:
            self.editor = None
            self.path = None
            self.logger.warning("RomFS is not valid! path=%s", path)

    def assert_rom_selected(self) -> bool:
        if self.editor is None:
            if self.path is None:
                return False

            self.select_rom(self.path)
            return self.assert_rom_selected()

        return True

    def open_scenario(self, scenario: Scenario):
        if not self.assert_rom_selected():
            self.logger.warning("No ROM selected!")
            return

        self.scenario = scenario
        self.brfld = self.editor.get_parsed_asset(scenario.scenario_file("brfld"), type_hint=Brfld)
        self.isScenarioLoaded = True

        self.actors.clear()

        self.bmmap = self.editor.get_parsed_asset(scenario.scenario_file("bmmap"), type_hint=Bmmap)
        self.bmsnav = self.editor.get_parsed_asset(scenario.scenario_file("bmsnav"), type_hint=Bmsnav)
        self.main_window.scenario_viewer.set_map_geo(self.bmsnav.raw.aNavmeshGeos, self.bmsnav.raw.areas, None, -1000)

        # draw map
        gridDef = self.bmmap.raw.Root.gridDef
        self.main_window.scenario_viewer.set_bounds(gridDef.vGridMin, gridDef.vGridMax)

        # TODO fix the bug where these disappear
        # might be fixed when i make it only use the outline and draw borders correctly?

        # for _, geo in self.bmmap.raw.Root.mapHeatRoomGeos.items():
        #     self.main_window.scenario_viewer.addMapGeo(geo.aVertex, geo.aIndex, QColor(255, 0, 0, 128), -900)

        # for _, geo in self.bmmap.raw.Root.mapEmmyRoomGeos.items():
        #     self.main_window.scenario_viewer.addMapGeo(geo.aVertex, geo.aIndex, QColor(0, 255, 0, 128), -900)

        # for _, outgeo in self.bmmap.raw.Root.mapOccluderGeos.items():
        #     print(type(outgeo))
        #     for _, geo in outgeo.items():
        #         self.main_window.scenario_viewer.addMapGeo(geo.aVertex, geo.aIndex, QColor(255, 255, 255, 128), -800)

        for layerName, layer in self.brfld.raw.Root.pScenario.items():
            if layerName in ["sLevelID", "sScenarioID", "vLayerFiles"]:
                continue

            for sublayerName, sublayer in layer.dctSublayers.items():
                for actorName, actorData in sublayer.dctActors.items():
                    actor = Actor(
                        ActorRef(self.scenario, layerName, sublayerName, actorName),
                        actorData,
                        self.editor,
                        self.main_window.actor_data_tree,
                        self.main_window.scenario_viewer,
                    )
                    self.actors.append(actor)
                    self.main_window.entity_list_tree.add_actor(actor)
                    self.main_window.scenario_viewer.add_actor(actor)

        self.bmscc = self.editor.get_parsed_asset(scenario.scenario_file("bmscc"), type_hint=Bmscc)
        ccs: dict[str, CollisionCameraItem] = {}
        for cc in self.bmscc.raw.layers[0].entries:
            ccs[cc.name] = self.main_window.scenario_viewer.add_collision_camera(cc)

        self.brsa = self.editor.get_parsed_asset(scenario.scenario_file("brsa"), type_hint=Brsa)
        for setup in self.brsa.raw.Root.pSubareaManager.vSubareaSetups:
            setup_id = setup.sId
            for subarea in setup.vSubareaConfigs:
                subarea_id = subarea.sId
                actor_groups = {
                    ActorLayer.LIGHTS: subarea.asItemsIds[1],
                    ActorLayer.SOUNDS: subarea.asItemsIds[2],
                    ActorLayer.ENTITIES: subarea.asItemsIds[4],
                }

                for actor_layer, actor_group_name in actor_groups.items():
                    if actor_group_name == "":
                        continue
                    try:
                        ag = self.brfld.get_actor_group(actor_group_name, actor_layer)
                        for actor_link in ag:
                            actor_link_parts = actor_link.split(":")
                            actor = self.get_actor_from_ref(
                                ActorRef(scenario, actor_link_parts[2], actor_link_parts[4], actor_link_parts[6])
                            )
                            actor.add_cc(setup_id, subarea_id)
                            self.main_window.subareas_list_tree.add_actor(
                                setup_id,
                                subarea_id,
                                actor_group_name,
                                actor,
                                ccs.get(subarea_id, None),
                            )
                    except KeyError:
                        self.logger.info("Missing actor group: %s", actor_group_name)
                        continue
        self.main_window.subareas_list_tree.root_node.setCheckState(0, Qt.CheckState.Checked)

    def get_actor_from_ref(self, ref: ActorRef) -> Actor | None:
        actors = [actor for actor in self.actors if actor.ref == ref]

        if len(actors) != 1:
            self.logger.warning("Actor not retrieved! Found %i matching actors", len(actors))
            return None

        return actors[0]

    def get_actor_def(self, adef: str) -> Bmsad:
        if adef.startswith("actordef:"):
            adef = adef[9:]

        return self.editor.get_parsed_asset(adef, type_hint=Bmsad)
