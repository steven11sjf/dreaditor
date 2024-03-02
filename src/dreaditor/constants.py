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

    def folder(self) -> str:
        return f"maps/levels/c010_samus/{self.value}"
    
    def brfld(self) -> str:
        return f"maps/levels/c010_samus/{self.value}/{self.value}.brfld"
    
    def bmmap(self) -> str:
        return f"maps/levels/c010_samus/{self.value}/{self.value}.bmmap"
    
    def bmscc(self) -> str:
        return f"maps/levels/c010_samus/{self.value}/{self.value}.bmscc"
    
    def bmscd(self) -> str:
        return f"maps/levels/c010_samus/{self.value}/{self.value}.bmscd"
    
    def bmssd(self) -> str:
        return f"maps/levels/c010_samus/{self.value}/{self.value}.bmssd"
    
    def model_folder(self) -> str:
        return f"maps/levels/c010_samus/{self.value}/models"

    def long_name(self) -> str:
        return self.name.title()