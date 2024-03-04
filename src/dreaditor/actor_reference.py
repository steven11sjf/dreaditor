import dataclasses
from mercury_engine_data_structures.formats.brfld import Brfld

from dreaditor.constants import Scenario

@dataclasses.dataclass()
class ActorRef:
    scenario: Scenario
    layer: str
    sublayer: str
    name: str