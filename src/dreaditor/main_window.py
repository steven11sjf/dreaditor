import logging
import os
from PyQt5.QtGui import QCloseEvent

from PyQt5.QtWidgets import QDockWidget, QFileDialog, QMainWindow, QMenu, QLabel, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt, QSize

from dreaditor import VERSION_STRING, get_log_folder, get_stylesheet
from dreaditor.constants import Scenario
from dreaditor.config import load_config, save_config
from dreaditor.entity_list_tree import EntityListTreeWidget
from dreaditor.rom_manager import RomManager


DEFAULT_WINDOW_DIMENSIONS: QSize = QSize(1280, 720)
MINIMUM_DOCK_WIDTH: int = 256

class DreaditorWindow(QMainWindow):
    actor_list_dock: QDockWidget
    entity_list_tree: EntityListTreeWidget
    central_dock: QDockWidget
    data_dock: QDockWidget

    rom_manager: RomManager

    def  __init__(self, *args, **kwargs):
        super(DreaditorWindow, self).__init__(*args, *kwargs)
        self.logger = logging.getLogger(type(self).__name__)
        load_config()
        self.rom_manager = RomManager()
        
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
        editMenu.addAction("Artaria").triggered.connect(lambda: self.openRegion(Scenario.ARTARIA))
        editMenu.addAction("Burenia").triggered.connect(lambda: self.openRegion(Scenario.BURENIA))
        editMenu.addAction("Cataris").triggered.connect(lambda: self.openRegion(Scenario.CATARIS))
        editMenu.addAction("Dairon").triggered.connect(lambda: self.openRegion(Scenario.DAIRON))
        editMenu.addAction("Elun").triggered.connect(lambda: self.openRegion(Scenario.ELUN))
        editMenu.addAction("Ferenia").triggered.connect(lambda: self.openRegion(Scenario.FERENIA))
        editMenu.addAction("Ghavoran").triggered.connect(lambda: self.openRegion(Scenario.GHAVORAN))
        editMenu.addAction("Hanubia").triggered.connect(lambda: self.openRegion(Scenario.HANUBIA))
        editMenu.addAction("Itorash").triggered.connect(lambda: self.openRegion(Scenario.ITORASH))

    def _createActorListDock(self):
        self.actor_list_dock = QDockWidget("Actors")
        self.actor_list_dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.actor_list_dock.setMinimumWidth(MINIMUM_DOCK_WIDTH)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.actor_list_dock)
        
        self.entity_list_tree = EntityListTreeWidget(self.rom_manager, None)
        self.actor_list_dock.setWidget(self.entity_list_tree)
    
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
        self.rom_manager.SelectRom(filename)

    def openLogFolder(self):
        self.logger.info("Opening logging dir")
        os.startfile(get_log_folder())

    def openRegion(self, region: Scenario):
        print(type(region))
        print(region)
        self.entity_list_tree.OnNewScenarioSelected(region)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        save_config()
        