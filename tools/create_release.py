from __future__ import annotations

from os import chdir
from shutil import make_archive

from importlib import metadata
from PyInstaller.__main__ import run

VERSION_STRING = metadata.version("dreaditor")

run(
    [
        "src/dreaditor/__main__.py",
        "--name",
        "Dreaditor-" + VERSION_STRING,
        "--add-data",
        "src/dreaditor/data:data",
        "--noconsole",
        "--clean",
        "--noconfirm",
    ]
)

chdir("dist")

make_archive("Dreaditor-" + VERSION_STRING, "zip", "Dreaditor-" + VERSION_STRING)

chdir("..")
