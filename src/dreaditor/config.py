import dreaditor
import json

CONFIG_FILE_NAME = "config.json"
_config = {}

def load_config():
    # TODO this is probably awful but it works for streamlining testing
    global _config
    filepath = dreaditor.get_appdata_folder().joinpath(CONFIG_FILE_NAME)

    if not filepath.exists():
        filepath.write_text("{}", "ascii")
    
    _config = json.loads(filepath.read_text())
    
def save_config():
    filepath = dreaditor.get_appdata_folder().joinpath(CONFIG_FILE_NAME)

    filepath.write_text(json.dumps(_config))

def get_config_data(key: str, default):
    result = _config.get(key, None)
    if result is None:
        _config[key] = default
        result = default
    return result

def set_config_data(key: str, val):
    _config[key] = val