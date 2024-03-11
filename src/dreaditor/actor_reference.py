import dataclasses
from mercury_engine_data_structures.formats.brfld import Brfld

from dreaditor.constants import Scenario

@dataclasses.dataclass()
class ActorRef:
    scenario: Scenario
    layer: str
    sublayer: str
    name: str

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        
        return (self.scenario == other.scenario
                and self.layer == other.layer
                and self.sublayer == other.sublayer
                and self.name == other.name)