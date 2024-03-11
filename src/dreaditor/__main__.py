import sys

from pathlib import Path
from PyQt5.QtWidgets import QApplication

from dreaditor import setup_logging, get_log_folder


log_dir = get_log_folder()
setup_logging("WARN", Path.joinpath(log_dir, "log.txt"))
with QApplication(sys.argv) as app:
    from dreaditor.main_window import DreaditorWindow

    window = DreaditorWindow()
    window.show()
    app.exec_()