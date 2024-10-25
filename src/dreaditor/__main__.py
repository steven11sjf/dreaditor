import sys

from pathlib import Path
from PySide6.QtWidgets import QApplication

from dreaditor import setup_logging, get_log_folder


log_dir = get_log_folder()
setup_logging("WARNING", "INFO", Path.joinpath(log_dir, "log.txt"))

from dreaditor.main_window import DreaditorWindow
app = QApplication(sys.argv)

window = DreaditorWindow()
window.show()
app.exec()