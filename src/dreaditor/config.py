from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING

import dreaditor

if TYPE_CHECKING:
    from pathlib import Path

CONFIG_FILE_NAME = "config.json"
DEFAULT_CONFIG = {
    "romfs_dir": None,
    "paintGeometry": True,
    "paintCollisionCameras": True,
    "paintDoors": True,
    "paintCollision": True,
    "paintBreakables": True,
    "paintLogicShapes": False,
    "paintLogicPaths": False,
    "paintWorldGraph": False,
    "paintPositionalSound": False,
}


class Config(dict):
    def __init__(self, config_path: Path):
        super().__init__()
        self.logger = logging.getLogger(type(self).__name__)
        self.config_path = config_path

        # load defaults
        self.update(DEFAULT_CONFIG)

        # load from file
        self._load()

    def _load(self):
        self.logger.info("Loading config from %s", self.config_path.as_posix())

        if self.config_path.exists():
            self.update(json.loads(self.config_path.read_text()))
        else:
            self.logger.warning("Config path (%s) does not exist!", self.config_path.as_posix())

    def _save(self):
        self.logger.info("Saving config to %s", self.config_path.as_posix())

        if not self.config_path.exists():
            self.logger.info("Creating config file at %s", self.config_path.as_posix())
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

        self.config_path.write_text(json.dumps(self, indent=4))

    def __setitem__(self, key, value) -> None:
        super().__setitem__(key, value)
        self.logger.info("Set %s to %s", key, value)
        self._save()


CurrentConfiguration = Config(dreaditor.get_appdata_folder().joinpath(CONFIG_FILE_NAME))
