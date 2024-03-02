import logging
import os

from PyQt5.QtWidgets import QDockWidget, QFileDialog, QMainWindow, QMenu, QLabel
from PyQt5.QtCore import Qt, QSize

from dreaditor import VERSION_STRING, get_log_folder, get_stylesheet
from dreaditor.constants import Scenario
from dreaditor.rom_manager import RomFS


DEFAULT_WINDOW_DIMENSIONS: QSize = QSize(1280, 720)
MINIMUM_DOCK_WIDTH: int = 256

class DreaditorWindow(QMainWindow):
    label: QLabel
    actor_list_dock: QDockWidget
    central_dock: QDockWidget
    data_dock: QDockWidget

    def  __init__(self, *args, **kwargs):
        super(DreaditorWindow, self).__init__(*args, *kwargs)
        self.logger = logging.getLogger(type(self).__name__)
        self.setWindowTitle(f"Dreaditor v{VERSION_STRING}")
        self.resize(DEFAULT_WINDOW_DIMENSIONS)
        self.setStyleSheet(get_stylesheet("main-window.txt"))

        self._createMenuBar()
        self._createActorListDock()
        self._createActorDetailsDock()
        self._createCentralDock()

        label = QLabel("Insert data here")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.central_dock)
        self.label = label

    def _createMenuBar(self):
        menuBar = self.menuBar()

        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        openRomAction = fileMenu.addAction("Select RomFS")
        openRomAction.triggered.connect(self.selectRomFS)
        openLogFolderAction = fileMenu.addAction("Open Log Folder")
        openLogFolderAction.triggered.connect(self.openLogFolder)

        editMenu = QMenu("&Select Scenario", self)
        menuBar.addMenu(editMenu)
        for region in Scenario:
            editMenu.addAction(region.long_name()).triggered.connect(lambda: self.openRegion(region))

    def _createActorListDock(self):
        self.actor_list_dock = QDockWidget("Actors")
        self.actor_list_dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.actor_list_dock.setMinimumWidth(MINIMUM_DOCK_WIDTH)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.actor_list_dock)
    
    def _createActorDetailsDock(self):
        self.data_dock = QDockWidget("Data")
        self.data_dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.data_dock.setMinimumWidth(MINIMUM_DOCK_WIDTH)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.data_dock)

    def _createCentralDock(self):
        self.central_dock = QDockWidget("Area Map")
        self.central_dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.central_dock)

    def selectRomFS(self):
        filename = QFileDialog.getExistingDirectory(self, "Open RomFS Folder")
        self.logger.info("Selected Directory: %s", filename)
        RomFS.SelectRom(filename)

    def openLogFolder(self):
        self.logger.info("Opening logging dir")
        os.startfile(get_log_folder())

    def openRegion(self, region: Scenario):
        RomFS.OpenScenario(region)