from enum import Enum
from dataclasses import dataclass

from lib.battle_board_game.units import Soldier


class CellTypes(Enum):
    FIELD = ('F', 0)
    SWAMP = ('S', -1)
    UNIT = ('U', None)


@dataclass
class Cell:
    type: str
    effect: int
    x: int
    y: int
    __soldier: Soldier

    @property
    def is_buzy(self):
        return bool(self.soldier)

    @property
    def soldier(self):
        return self.__soldier

    @soldier.setter
    def soldier(self, new_soldier):
        if self.is_buzy:
            raise AttributeError(f'Cell with coords {self.x}, {self.y} is buzy')
        self.__soldier = new_soldier
