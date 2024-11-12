from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dreaditor.constants import Scenario


@dataclasses.dataclass()
class ActorRef:
    scenario: Scenario
    layer: str
    sublayer: str
    name: str

    def __eq__(self, other):
        if not isinstance(other, ActorRef):
            return False

        return (
            self.scenario == other.scenario
            and self.layer == other.layer
            and self.sublayer == other.sublayer
            and self.name == other.name
        )

    def __repr__(self) -> str:
        return f"{self.scenario.name}/{self.layer}/{self.sublayer}/{self.name}"
