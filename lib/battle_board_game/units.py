from collections import namedtuple
from dataclasses import dataclass
from enum import Enum, auto

from lib.battle_board_game.board import Cell


class FightResults(Enum):
    ATTAKER_FAILED = auto()
    ATTAKER_WON = auto()
    BOTH_ALIVE = auto()
    BOTH_DEAD = auto()


class SoldierType(Enum):
    SMALL_MILLY = 'small_milly'
    BIG_MILLY = 'big_milly'


UiSoldierInfo = namedtuple('UiSoldierInfo', ['type', 'start_x', 'start_y'])
FightBounty = namedtuple('FightBounty', ['attacker_reward', 'defender_reward'])


class Player:
    def __init__(self):
        self.soldiers: list = []
        self.score: int = 0

    def is_winner(self, game):
        return game.win_score <= self.score

    def react_on_fight(self, bounty: int):
        self.score += bounty


@dataclass()
class Soldier:
    type: SoldierType
    health: int = 0
    damage: int = 0
    bounty: int = 0
    speed: int = 0
    current_cell: Cell = None
    player: Player = None

    def hit(self, defender: 'Soldier') -> FightBounty:
        defender.take_damage(self.damage_on_cell)
        self.take_damage(defender.damage_on_defend)
        return FightBounty(
            attacker_reward=defender.reward_after_hight,
            defender_reward=self.reward_after_hight
        )

    def take_damage(self, damage):
        if damage > 0:
            self.health -= damage

    @property
    def damage_on_cell(self):
        if self.damage + self.current_cell.effect > 0:
            return self.damage + self.current_cell.effect
        return 0

    @property
    def damage_on_defend(self):
        if self.current_cell.effect > 0:
            return self.current_cell.effect
        return 0

    @property
    def is_dead(self):
        return self.health <= 0

    @property
    def is_alive(self):
        return not self.is_dead

    @property
    def reward_after_hight(self):
        return self.bounty * int(self.is_dead)


class ArmyFactory:
    SOLDIERS = {
        SoldierType.SMALL_MILLY: {
            'health': 4,
            'damage': 2,
            'speed': 2,
            'bounty': 1
        },
        SoldierType.BIG_MILLY: {
            'health': 7,
            'damage': 3,
            'speed': 1,
            'bounty': 2
        }
    }

    def __init__(self, board):
        self.board = board
        self.army = []

    def produce(self, base_info: list[UiSoldierInfo], player: Player) -> list[Soldier]:
        self.army.clear()
        for soldier in base_info:
            if soldier.type not in SoldierType:
                raise AttributeError(f'Invalid SoldierType: {soldier.type}')

            cell = self.board.get_cell(x=soldier.start_x, y=soldier.start_y)
            if not cell:
                raise AttributeError(f'Cell with coords {soldier.start_x}, {soldier.start_y} does not exist')

            soldier = Soldier(
                **self.SOLDIERS[soldier.type],
                type=soldier.type,
                current_cell=cell,
                player=player
            )
            cell.soldier = soldier
            self.army.append(soldier)
        return self.army
