import logging
from pathlib import Path

from mercury_engine_data_structures.file_tree_editor import FileTreeEditor
from mercury_engine_data_structures.game_check import Game

from dreaditor.constants import Scenario


class RomManager:
    editor: FileTreeEditor
    path: str

    def __init__(self):
        self.logger = logging.getLogger(type(self).__name__)
        self.editor = None
        self.path = None
        self.logger.error("please fucking show up")
    
    def SelectRom(self, path: str):
        self.path = path
        try:
            self.editor = FileTreeEditor(Path(path), target_game=Game.DREAD)
        except:
            self.editor = None
            self.path = None
            self.logger.error("RomFS is not valid! path=%s", path)
            print("asdf")

    def AssertRomSelected(self) -> bool:
        if self.editor is None:
            if self.path is None:
                return False
            
            self.SelectRom(self.path)
            return self.AssertRomSelected()
        
        return True
    
    def OpenScenario(self, scenario: Scenario):
        if not self.AssertRomSelected():
            self.logger.error("No ROM selected!")
    

RomFS: RomManager = RomManager()