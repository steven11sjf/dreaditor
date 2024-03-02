from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtCore import Qt

from dreaditor.constants import Scenario
from dreaditor.rom_manager import RomManager


class EntityListTreeWidget(QTreeWidget):
    rom_manager: RomManager | None

    def __init__(self, rom_manager: RomManager, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.setHeaderHidden(True)

        self.rom_manager = rom_manager
    
    def OnNewScenarioSelected(self, scenario: Scenario):
        brfld, bmmap = self.rom_manager.OpenScenario(scenario)

        # guard against no scenario selected
        if brfld is None:
            return
        
        self.clear()

        # add brfld data
        brfldItem = QTreeWidgetItem(["BRFLD"])
        brfldItem.setFlags(brfldItem.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
        brfldItem.setCheckState(0, Qt.CheckState.Unchecked)

        for layerName, layer in brfld.raw.Root.pScenario.items():
            if layerName in ["sLevelID", "sScenarioID", "vLayerFiles"]:
                continue
            
            layerItem = QTreeWidgetItem([layerName])
            layerItem.setFlags(layerItem.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
            layerItem.setCheckState(0, Qt.CheckState.Unchecked)
            brfldItem.addChild(layerItem)

            for sublayerName, sublayer in layer.dctSublayers.items():
                sublayerItem = QTreeWidgetItem([sublayerName])
                sublayerItem.setFlags(sublayerItem.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
                sublayerItem.setCheckState(0, Qt.CheckState.Unchecked)
                layerItem.addChild(sublayerItem)

                for actorName, _ in sublayer.dctActors.items():
                    actorItem = QTreeWidgetItem([actorName])
                    actorItem.setFlags(sublayerItem.flags() | Qt.ItemFlag.ItemIsAutoTristate | Qt.ItemFlag.ItemIsUserCheckable)
                    actorItem.setCheckState(0, Qt.CheckState.Unchecked)
                    sublayerItem.addChild(actorItem)
        
        self.addTopLevelItem(brfldItem)