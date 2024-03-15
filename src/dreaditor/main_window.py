import logging
import os
from PyQt5.QtGui import QCloseEvent

from PyQt5.QtWidgets import QDockWidget, QFileDialog, QMainWindow, QMenu, QLabel, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt, QSize

from dreaditor import VERSION_STRING, get_log_folder, get_stylesheet
from dreaditor.actor_reference import ActorRef
from dreaditor.constants import Scenario, ScenarioHelpers
from dreaditor.config import load_config, save_config
from dreaditor.widgets.actor_data_tree import ActorDataTreeWidget
from dreaditor.widgets.entity_list_tree import EntityListTreeWidget
from dreaditor.widgets.scenario_viewer import ScenarioViewer
from dreaditor.widgets.scenario_scene import ScenarioScene
from dreaditor.rom_manager import RomManager


DEFAULT_WINDOW_DIMENSIONS: QSize = QSize(1280, 720)
MINIMUM_DOCK_WIDTH: int = 256

class DreaditorWindow(QMainWindow):
    actor_list_dock: QDockWidget
    entity_list_tree: EntityListTreeWidget
    central_dock: QDockWidget
    data_dock: QDockWidget
    actor_data_tree: ActorDataTreeWidget
    scenario_viewer: ScenarioViewer

    rom_manager: RomManager

    def  __init__(self, *args, **kwargs):
        super(DreaditorWindow, self).__init__(*args, *kwargs)
        self.logger = logging.getLogger(type(self).__name__)
        load_config()
        self.rom_manager = RomManager(self)
        
        self.setWindowTitle(f"Dreaditor v{VERSION_STRING}")
        self.resize(DEFAULT_WINDOW_DIMENSIONS)
        self.setStyleSheet(get_stylesheet("main-window.txt"))

        # create menu bar
        menuBar = self.menuBar()

        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction("Select RomFS").triggered.connect(self.selectRomFS)
        fileMenu.addAction("Open Log Folder").triggered.connect(self.openLogFolder)

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

        # create actor details dock
        self.data_dock = QDockWidget("Data")
        self.data_dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.data_dock.setMinimumWidth(MINIMUM_DOCK_WIDTH)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.data_dock)

        self.actor_data_tree = ActorDataTreeWidget(self.rom_manager, None)
        self.data_dock.setWidget(self.actor_data_tree)

        # create entity list dock
        self.actor_list_dock = QDockWidget("Actors")
        self.actor_list_dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.actor_list_dock.setMinimumWidth(MINIMUM_DOCK_WIDTH)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.actor_list_dock)
        
        self.entity_list_tree = EntityListTreeWidget(self.actor_data_tree, None)
        self.actor_list_dock.setWidget(self.entity_list_tree)

        # create central dock
        self.central_dock = QDockWidget("Area Map")
        self.central_dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.central_dock)

        self.scenario_viewer = ScenarioViewer(ScenarioScene(), self.rom_manager)
        self.central_dock.setWidget(self.scenario_viewer)
        self.setCentralWidget(self.central_dock)

    def selectRomFS(self):
        filename = QFileDialog.getExistingDirectory(self, "Open RomFS Folder")
        self.logger.info("Selected Directory: %s", filename)
        self.rom_manager.SelectRom(filename)

    def openLogFolder(self):
        self.logger.info("Opening logging dir")
        os.startfile(get_log_folder())

    def openRegion(self, scenario: Scenario):
        self.setWindowTitle(f"Dreaditor v{VERSION_STRING}: {ScenarioHelpers.long_name(scenario)}")
        self.entity_list_tree.OnNewScenarioSelected()
        self.scenario_viewer.OnNewScenarioSelected(scenario)
        self.actor_data_tree.clear()
        self.rom_manager.OpenScenario(scenario)

    def SelectNode(self, layer: str, sublayer: str, sName: str):
        self.entity_list_tree.SelectBrfldNode(layer, sublayer, sName)
        self.actor_data_tree.LoadActor(ActorRef(self.rom_manager.scenario, layer, sublayer, sName))

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        save_config()
        