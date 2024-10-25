from __future__ import annotations

from enum import Enum
from mercury_engine_data_structures.game_check import GameVersion



class Scenario(Enum):
    game_versions: list[GameVersion]

    ARTARIA = "s010_cave"
    BURENIA = "s040_aqua"
    CATARIS = "s020_magma"
    DAIRON = "s030_baselab"
    ELUN = "s060_quarantine"
    FERENIA = "s070_basesanc"
    GHAVORAN = "s050_forest"
    HANUBIA = "s080_shipyard"
    ITORASH = "s090_skybase"
    CORPIUS_BOSS_RUSH = "s201_bossrush_scorpius", [GameVersion.DREAD_2_1_0]
    KRAID_BOSS_RUSH = "s202_bossrush_kraid", [GameVersion.DREAD_2_1_0]
    ARTARIA_CENTRAL_UNIT_BOSS_RUSH = "s203_bossrush_cu_artaria", [GameVersion.DREAD_2_1_0]
    DROGYGA_BOSS_RUSH = "s204_bossrush_drogyga", [GameVersion.DREAD_2_1_0]
    GOLD_ROBOT_BOSS_RUSH = "s205_bossrush_strong_rcs", [GameVersion.DREAD_2_1_0]
    ESCUE_BOSS_RUSH =  "s206_bossrush_escue", [GameVersion.DREAD_2_1_0]
    EXPERIMENT_Z57_BOSS_RUSH = "s207_bossrush_cooldownx", [GameVersion.DREAD_2_1_0]
    DOUBLE_ROBOTS_BOSS_RUSH = "s208_bossrush_strong_rcs_x2", [GameVersion.DREAD_2_1_0]
    GOLZUNA_BOSS_RUSH = "s209_bossrush_golzuna", [GameVersion.DREAD_2_1_0]
    ELITE_CHOZO_BOSS_RUSH = "s210_bossrush_elite_cwx", [GameVersion.DREAD_2_1_0]
    FERENIA_CENTRAL_UNIT_BOSS_RUSH = "s211_bossrush_cu_ferenia", [GameVersion.DREAD_2_1_0]
    COMMANDER_BOSS_RUSH = "s212_bossrush_commander", [GameVersion.DREAD_2_1_0]

    def __new__(cls, value: str, versions: list[GameVersion] = None) -> Scenario:
        member = object.__new__(cls)
        member._value_ = value

        if versions == None:
            versions = [
                GameVersion.DREAD_1_0_0, 
                GameVersion.DREAD_1_0_1, 
                GameVersion.DREAD_2_0_0, 
                GameVersion.DREAD_2_1_0
            ]

        member.game_versions = versions

        return member

    def scenario_file(self, extension: str) -> str:
        return f"maps/levels/c10_samus/{self.value}/{self.value}.{extension}"

    @property
    def long_name(self) -> str:
        return " ".join(self.name.split("_")).title()