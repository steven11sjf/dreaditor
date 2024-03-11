import logging

from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import Qt, pyqtSlot


class ScenarioScene(QGraphicsScene):

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(type(self).__name__)
        self.logger.info("Initialized ScenarioScene!")