from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
from pathlib import Path

from dreaditor import setup_logging, get_log_folder


log_dir = get_log_folder() # TODO save logs somewhere
setup_logging("DEBUG", Path.joinpath(log_dir, "log.txt"))
with QApplication(sys.argv) as app:
    from dreaditor.main_window import DreaditorWindow

    window = DreaditorWindow()
    window.show()
    app.exec_()