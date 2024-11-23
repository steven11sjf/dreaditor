from __future__ import annotations

from PySide6.QtCore import QPointF


def vector2f(data: list[float]):
    return QPointF(data[0], -data[1])
