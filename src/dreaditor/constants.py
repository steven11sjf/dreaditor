from __future__ import annotations

from enum import Enum
from mercury_engine_data_structures.game_check import GameVersion



class Scenario(Enum):
    game_versions: list[GameVersion]
    long_name: str

    ARTARIA = "s010_cave", "Artaria"
    BURENIA = "s040_aqua", "Burenia"
    CATARIS = "s020_magma", "Cataris"
    DAIRON = "s030_baselab", "Dairon"
    ELUN = "s060_quarantine", "Elun"
    FERENIA = "s070_basesanc", "Ferenia"
    GHAVORAN = "s050_forest", "Ghavoran"
    HANUBIA = "s080_shipyard", "Hanubia"
    ITORASH = "s090_skybase", "Itorash"
    BOSSRUSH_CORPIUS = "s201_bossrush_scorpius", "Corpius Bossrush", [GameVersion.DREAD_2_1_0]
    BOSSRUSH_KRAID = "s202_bossrush_kraid", "Kraid Bossrush", [GameVersion.DREAD_2_1_0]
    BOSSRUSH_ARTARIA_CU = "s203_bossrush_cu_artaria", "Artaria CU Bossrush", [GameVersion.DREAD_2_1_0]
    BOSSRUSH_DROGYGA = "s204_bossrush_drogyga", "Drogyga Bossrush", [GameVersion.DREAD_2_1_0]
    BOSSRUSH_STRONG_RCS = "s205_bossrush_strong_rcs", "Gold Robot Bossrush", [GameVersion.DREAD_2_1_0]
    BOSSRUSH_ESCUE =  "s206_bossrush_escue", "Escue Bossrush", [GameVersion.DREAD_2_1_0]
    BOSSRUSH_COOLDOWNX = "s207_bossrush_cooldownx", "Experiment Z57 Bossrush", [GameVersion.DREAD_2_1_0]
    BOSSRUSH_STRONG_RCS_X2 = "s208_bossrush_strong_rcs_x2", "Double Robots Bossrush", [GameVersion.DREAD_2_1_0]
    BOSSRUSH_GOLZUNA = "s209_bossrush_golzuna", "Golzuna Bossrush", [GameVersion.DREAD_2_1_0]
    BOSSRUSH_ELITE_CWX = "s210_bossrush_elite_cwx", "Elite Chozo Bossrush", [GameVersion.DREAD_2_1_0]
    BOSSRUSH_FERENIA_CU = "s211_bossrush_cu_ferenia", "Ferenia CU Bossrush", [GameVersion.DREAD_2_1_0]
    BOSSRUSH_COMMANDER = "s212_bossrush_commander", "Raven Beak Bossrush", [GameVersion.DREAD_2_1_0]

    def __new__(cls, value: str, long_name: str = None, versions: list[GameVersion] = None) -> Scenario:
        member = object.__new__(cls)
        member._value_ = value
        member.long_name = long_name

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
