from __future__ import annotations

import logging

from PySide6.QtWidgets import QGraphicsScene


class ScenarioScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(type(self).__name__)
        self.logger.info("Initialized ScenarioScene!")
