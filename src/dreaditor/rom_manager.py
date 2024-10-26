from __future__ import annotations
from typing import TYPE_CHECKING

import logging
from pathlib import Path

from mercury_engine_data_structures.file_tree_editor import FileTreeEditor
from mercury_engine_data_structures.formats.bmmap import Bmmap
from mercury_engine_data_structures.formats.bmscc import Bmscc
from mercury_engine_data_structures.formats.bmsad import Bmsad
from mercury_engine_data_structures.formats.brfld import Brfld, ActorLayer
from mercury_engine_data_structures.formats.brsa import Brsa
from mercury_engine_data_structures.game_check import Game
from mercury_engine_data_structures.romfs import ExtractedRomFs

from dreaditor.actor import Actor
from dreaditor.actor_reference import ActorRef
from dreaditor.constants import Scenario
from dreaditor.config import get_config_data, set_config_data

if TYPE_CHECKING:
    from dreaditor.main_window import DreaditorWindow

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
        self.path = get_config_data("romfs_dir")
        self.logger.info("Path loaded from config: %s", self.path)
        self.actors = []
        self.SelectRom(self.path)
    
    def SelectRom(self, path: str):
        self.path = path
        try:
            self.editor = FileTreeEditor(ExtractedRomFs(Path(path)), target_game=Game.DREAD)
            set_config_data("romfs_dir", path)
            self.logger.info(f"Selected RomFS at {path} with version {self.editor.version}")
        except:
            self.editor = None
            self.path = None
            self.logger.warning("RomFS is not valid! path=%s", path)

    def AssertRomSelected(self) -> bool:
        if self.editor is None:
            if self.path is None:
                return False
            
            self.SelectRom(self.path)
            return self.AssertRomSelected()

        return True
    
    def OpenScenario(self, scenario: Scenario):
        if not self.AssertRomSelected():
            self.logger.warning("No ROM selected!")
            return

        self.scenario = scenario
        self.brfld = self.editor.get_parsed_asset(scenario.scenario_file("brfld"), type_hint=Brfld)
        self.isScenarioLoaded = True

        self.actors.clear()

        self.bmmap = self.editor.get_parsed_asset(scenario.scenario_file("bmmap"), type_hint=Bmmap)

        # draw map
        gridDef = self.bmmap.raw.Root.gridDef
        self.main_window.scenario_viewer.setBounds(gridDef.vGridMin, gridDef.vGridMax)
        for geo in self.bmmap.raw.Root.aNavmeshGeos:
            self.main_window.scenario_viewer.addMapGeo(geo.aVertex, geo.aIndex, None, -1000)

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
                    actor = Actor(ActorRef(self.scenario, layerName, sublayerName, actorName), actorData, self.editor, self.main_window.actor_data_tree, self.main_window.scenario_viewer)
                    self.actors.append(actor)
                    self.main_window.entity_list_tree.addBrfldItem(actor)
                    self.main_window.scenario_viewer.addActor(actor)

        self.bmscc = self.editor.get_parsed_asset(scenario.scenario_file("bmscc"), type_hint=Bmscc)
        ccs: dict[str, dict] = {cc.name: cc for cc in self.bmscc.raw.layers[0].entries}

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
                            self.main_window.subareas_list_tree.add_item(
                                setup_id, 
                                subarea_id, 
                                actor_group_name,
                                self.GetActorFromRef(ActorRef(scenario, actor_link_parts[2], actor_link_parts[4], actor_link_parts[6]))
                            )
                    except KeyError:
                        self.logger.info("Missing actor group: %s", actor_group_name)
                        continue

        
    
    def GetActorFromRef(self, ref: ActorRef) -> Actor | None:
        actors = [actor for actor in self.actors if actor.ref == ref]

        if len(actors) != 1:
            self.logger.warning("Actor not retrieved! Found %i matching actors", len(actors))
            return None
        
        return actors[0]
    
    def GetActorDef(self, adef: str) -> Bmsad:
        if adef.startswith("actordef:"):
            adef = adef[9:]
        
        return self.editor.get_parsed_asset(adef, type_hint=Bmsad)
    
    def SelectNode(self, layer: str, sublayer: str, sName: str):
        self.logger.info("SelectNode called: (%s, %s, %s)", layer, sublayer, sName)
        self.main_window.SelectNode(layer, sublayer, sName)