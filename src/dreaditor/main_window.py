from __future__ import annotations

import logging
import os

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QCloseEvent
from PySide6.QtWidgets import QDockWidget, QFileDialog, QMainWindow, QMenu, QTabWidget

from dreaditor import VERSION_STRING, get_log_folder, get_stylesheet
from dreaditor.config import get_config_data, save_config, set_config_data
from dreaditor.constants import Scenario
from dreaditor.rom_manager import RomManager
from dreaditor.widgets.actor_data_tree import ActorDataTreeWidget
from dreaditor.widgets.entity_list_tree import EntityListTreeWidget
from dreaditor.widgets.scenario_scene import ScenarioScene
from dreaditor.widgets.scenario_viewer import ScenarioViewer
from dreaditor.widgets.subareas_list_tree import SubareasListTree

DEFAULT_WINDOW_DIMENSIONS: QSize = QSize(1280, 720)
MINIMUM_DOCK_WIDTH: int = 256


class DreaditorWindow(QMainWindow):
    edit_menu: QMenu
    scenario_actions: dict[Scenario, QAction]

    actor_list_dock: QDockWidget
    entity_list_tree: EntityListTreeWidget
    central_dock: QDockWidget
    data_dock: QDockWidget
    actor_data_tree: ActorDataTreeWidget
    scenario_viewer: ScenarioViewer

    rom_manager: RomManager

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.logger = logging.getLogger(type(self).__name__)
        self.rom_manager = RomManager(self)

        self.setWindowTitle(f"Dreaditor v{VERSION_STRING}")
        self.resize(DEFAULT_WINDOW_DIMENSIONS)
        self.setStyleSheet(get_stylesheet("main-window.txt"))
        self.setTabPosition(Qt.DockWidgetArea.LeftDockWidgetArea, QTabWidget.TabPosition.North)

        # create menu bar
        menuBar = self.menuBar()

        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction("Select RomFS").triggered.connect(self.select_rom_fs)
        fileMenu.addAction("Open Log Folder").triggered.connect(self.open_log_folder)

        self.edit_menu = QMenu("&Load Scenario", self)
        menuBar.addMenu(self.edit_menu)

        # helper to add edit menu functions and link the scenario enums
        def _add_edit_menu_action(region: Scenario, actions: dict[Scenario, QAction]):
            action = QAction(region.long_name)
            action.triggered.connect(lambda: self.open_region(region))
            actions[region] = action

        self.scenario_actions = {}
        for s in Scenario:
            _add_edit_menu_action(s, self.scenario_actions)

        paintMenu = QMenu("&Painting Options", self)
        menuBar.addMenu(paintMenu)

        # helper to add paint menu functions and link the config values
        def _add_paint_menu_action(text: str, config_name: str):
            action = QAction(text, paintMenu)
            action.setCheckable(True)
            action.setChecked(get_config_data(config_name))
            action.triggered.connect(lambda checked: self.on_paint_option_triggered(checked, config_name))
            paintMenu.addAction(action)

        _add_paint_menu_action("Static Geometry", "paintGeometry")
        _add_paint_menu_action("Collision Cameras", "paintCollisionCameras")
        _add_paint_menu_action("Doors", "paintDoors")
        _add_paint_menu_action("Collision", "paintCollision")
        _add_paint_menu_action("Breakable Tiles", "paintBreakables")
        _add_paint_menu_action("Logic Shapes", "paintLogicShapes")
        _add_paint_menu_action("Logic Paths", "paintLogicPaths")
        _add_paint_menu_action("World Graph", "paintWorldGraph")
        _add_paint_menu_action("Positional Sounds", "paintPositionalSound")

        self.update_menu_for_rom_versions()

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

        # create subareas dock
        self.subareas_dock = QDockWidget("Subareas")
        self.subareas_dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.subareas_dock.setMinimumWidth(MINIMUM_DOCK_WIDTH)
        self.tabifyDockWidget(self.actor_list_dock, self.subareas_dock)

        self.subareas_list_tree = SubareasListTree(self.actor_data_tree, None)
        self.subareas_dock.setWidget(self.subareas_list_tree)

        # ensure actors dock is the default left-side dock
        self.actor_list_dock.raise_()

        # create central dock
        self.central_dock = QDockWidget("Area Map")
        self.central_dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.central_dock)

        self.scenario_viewer = ScenarioViewer(ScenarioScene(), self.rom_manager)
        self.central_dock.setWidget(self.scenario_viewer)
        self.setCentralWidget(self.central_dock)

    def on_paint_option_triggered(self, checked: bool, config_name: str):
        set_config_data(config_name, checked)
        self.scenario_viewer.viewport().update()

    def select_rom_fs(self):
        filename = QFileDialog.getExistingDirectory(self, "Open RomFS Folder")
        self.logger.info("Selected Directory: %s", filename)
        self.rom_manager.select_rom(filename)
        self.update_menu_for_rom_versions()

    def update_menu_for_rom_versions(self):
        for act in self.edit_menu.actions():
            self.edit_menu.removeAction(act)

        if self.rom_manager.editor:
            ver = self.rom_manager.editor.version
            for scenario, action in self.scenario_actions.items():
                if ver in scenario.game_versions:
                    self.edit_menu.addAction(action)

    def open_log_folder(self):
        self.logger.info("Opening logging dir")
        os.startfile(get_log_folder())

    def open_region(self, scenario: Scenario):
        self.setWindowTitle(f"Dreaditor v{VERSION_STRING}: {scenario.long_name}")
        self.entity_list_tree.on_new_scenario_selected()
        self.subareas_list_tree.on_new_scenario_selected()
        self.scenario_viewer.on_new_scenario_selected(scenario)
        self.actor_data_tree.clear()
        self.rom_manager.open_scenario(scenario)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        save_config()
