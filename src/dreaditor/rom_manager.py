import logging
from pathlib import Path

from mercury_engine_data_structures.file_tree_editor import FileTreeEditor
from mercury_engine_data_structures.formats.brfld import Brfld
from mercury_engine_data_structures.formats.bmmap import Bmmap
from mercury_engine_data_structures.game_check import Game

from dreaditor.constants import Scenario, ScenarioHelpers


class RomManager:
    editor: FileTreeEditor | None
    path: str | None

    def __init__(self):
        self.logger = logging.getLogger(type(self).__name__)
        self.editor = None
        self.path = None
    
    def SelectRom(self, path: str):
        self.path = path
        try:
            self.editor = FileTreeEditor(Path(path), target_game=Game.DREAD)
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

        return (
            self.editor.get_parsed_asset(ScenarioHelpers.brfld(scenario), type_hint=Brfld),
            self.editor.get_parsed_asset(ScenarioHelpers.bmmap(scenario), type_hint=Bmmap),
        )
        

    

RomFS: RomManager = RomManager()