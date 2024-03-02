from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
from pathlib import Path

from dreaditor import setup_logging, get_log_folder
from dreaditor.main_window import DreaditorWindow


log_dir = get_log_folder() # TODO save logs somewhere
setup_logging("DEBUG", Path.joinpath(log_dir, "log.txt"))
app = QApplication(sys.argv)

window = DreaditorWindow()
window.show()

app.exec_()