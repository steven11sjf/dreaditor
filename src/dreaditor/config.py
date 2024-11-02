from __future__ import annotations

import json

import dreaditor

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

config_path = dreaditor.get_appdata_folder().joinpath(CONFIG_FILE_NAME)
if not config_path.exists():
    config_path.write_text(json.dumps(DEFAULT_CONFIG), "ascii")

_config = json.loads(config_path.read_text())


def save_config():
    filepath = dreaditor.get_appdata_folder().joinpath(CONFIG_FILE_NAME)

    filepath.write_text(json.dumps(_config, indent=4))


def get_config_data(key: str):
    result = _config.get(key, None)
    if result is None:
        _config[key] = DEFAULT_CONFIG[key]
        result = DEFAULT_CONFIG[key]
    return result


def set_config_data(key: str, val):
    _config[key] = val
