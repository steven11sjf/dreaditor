from __future__ import annotations
from typing import TYPE_CHECKING

import logging
from pathlib import Path

from mercury_engine_data_structures.file_tree_editor import FileTreeEditor
from mercury_engine_data_structures.formats.brfld import Brfld
from mercury_engine_data_structures.formats.bmmap import Bmmap
from mercury_engine_data_structures.game_check import Game

from dreaditor.constants import Scenario, ScenarioHelpers
from dreaditor.config import get_config_data, set_config_data

if TYPE_CHECKING:
    from dreaditor.main_window import DreaditorWindow

class RomManager:
    main_window: DreaditorWindow
    editor: FileTreeEditor | None
    path: str | None

    isScenarioLoaded: bool = False
    scenario: Scenario | None
    brfld: Brfld | None

    def __init__(self, main_window: DreaditorWindow):
        self.logger = logging.getLogger(type(self).__name__)
        self.main_window = main_window
        self.editor = None
        self.path = get_config_data("romfs_dir", None)
        self.logger.info("Path is %s", self.path)
        self.SelectRom(self.path)
    
    def SelectRom(self, path: str):
        self.path = path
        try:
            self.editor = FileTreeEditor(Path(path), target_game=Game.DREAD)
            set_config_data("romfs_dir", path)
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
    
    def OpenScenario(self, scenario: Scenario) -> tuple[Brfld, Bmmap]:
        if not self.AssertRomSelected():
            self.logger.warning("No ROM selected!")
            return (None, None)

        self.scenario = scenario
        self.brfld = self.editor.get_parsed_asset(ScenarioHelpers.brfld(scenario), type_hint=Brfld)
        self.isScenarioLoaded = True

        return (
            self.editor.get_parsed_asset(ScenarioHelpers.brfld(scenario), type_hint=Brfld),
            self.editor.get_parsed_asset(ScenarioHelpers.bmmap(scenario), type_hint=Bmmap),
        )
    
    def SelectNode(self, layer: str, sublayer: str, sName: str):
        self.logger.info("SelectNode called: (%s, %s, %s)", layer, sublayer, sName)
        self.main_window.SelectNode(layer, sublayer, sName)