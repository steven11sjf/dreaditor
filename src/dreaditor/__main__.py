from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from dreaditor import get_log_folder, setup_logging
from dreaditor.main_window import DreaditorWindow

log_dir = get_log_folder()
setup_logging("WARNING", "INFO", Path.joinpath(log_dir, "log.txt"))


app = QApplication(sys.argv)

window = DreaditorWindow()
window.show()
app.exec()
