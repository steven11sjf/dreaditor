from enum import Enum


class Scenario(Enum):
    ARTARIA = "s010_cave"
    BURENIA = "s040_aqua"
    CATARIS = "s020_magma"
    DAIRON = "s030_baselab"
    ELUN = "s060_quarantine"
    FERENIA = "s070_basesanc"
    GHAVORAN = "s050_forest"
    HANUBIA = "s080_shipyard"
    ITORASH = "s090_skybase"

class ScenarioHelpers:
    @classmethod
    def folder(cls, scenario: Scenario) -> str:
        return f"maps/levels/c10_samus/{scenario.value}"
    
    @classmethod
    def brfld(cls, scenario: Scenario) -> str:
        return f"maps/levels/c10_samus/{scenario.value}/{scenario.value}.brfld"
    
    @classmethod
    def bmmap(cls, scenario: Scenario) -> str:
        return f"maps/levels/c10_samus/{scenario.value}/{scenario.value}.bmmap"

    @classmethod
    def long_name(cls, scenario: Scenario) -> str:
        return scenario.name.title()
