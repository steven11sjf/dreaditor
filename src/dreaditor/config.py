from pathlib import Path

import dreaditor



class Configuration:
    romfs_path: Path
    last_viewed_map: str
    last_map_views: dict[str, str]