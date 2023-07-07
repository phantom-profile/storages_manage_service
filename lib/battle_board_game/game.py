from enum import Enum, auto

from lib.battle_board_game.units import Player, ArmyFactory, Soldier, FightResults


class Actions(Enum):
    MOVE = auto()
    FIGHT = auto()

    class ActionError(BaseException):
        ...


class SoldiersFightService:
    def __init__(
        self,
        attacker: Soldier,
        defender: Soldier,
        attacker_player: Player,
        defender_player: Player,
        board
    ):
        self.attaker = attacker
        self.defender = defender
        self.attaker_player = attacker_player
        self.defender_player = defender_player
        self.board = board

    def perform(self):
        if not self.board.check_if_cells_near(self.attaker.current_cell, self.defender.current_cell):
            raise Actions.ActionError('Cells are not near each other, fight impossible')
        if self.attaker.is_dead or self.defender.is_dead:
            raise Actions.ActionError('one of soldiers is dead, impossible to fight')

        result = self.attaker.hit(self.defender)
        self.attaker_player.react_on_fight(result.attacker_reward)
        self.defender_player.react_on_fight(result.defender_reward)


class SoldierMoveService:
    def __init__(self, soldier: Soldier, board, target_x: int, target_y: int):
        self.soldier = soldier
        self.board = board
        self.x = target_x
        self.y = target_y

    def perform(self):
        cell = self.board.get_cell(x=self.x, y=self.y)
        if not cell:
            raise Actions.ActionError(f'Cell with coords {self.x}, {self.y} does not exist')
        if not self.are_cells_in_distance(cell):
            raise Actions.ActionError(f'Cell with coords {self.x}, {self.y} unreacheble')

        self.soldier.current_cell = cell
        cell.soldier = self.soldier

    def are_cells_in_distance(self, cell):
        x_move = abs(cell.x - self.soldier.current_cell.x)
        y_move = abs(cell.y - self.soldier.current_cell.y)
        if x_move + y_move <= self.soldier.speed:
            return True


class Game:
    def __init__(self, players_number, win_score, board, ui, army_factory):
        self.players_number: int = players_number
        self.players: list[Player] = []
        self.win_score: int = win_score
        self.board = board
        self.army_factory = army_factory(self.board)
        self.ui = ui
        self.winner = None

    def start_game(self):
        for i in range(self.players_number):
            self.prepare_player()
        while not self.game_finished():
            self.make_turn()
        self.finish_game()

    def prepare_player(self):
        player = Player()
        player.soldiers = self.army_factory.produce(
            base_info=self.ui.get_army_info,
            player=player
        )
        self.players.append(player)

    def make_turn(self):
        for player in self.players:
            self.ui.announce_turn(player)
            for soldier in player.soldiers:
                action = self.ui.get_action()
                if action == Actions.MOVE:
                    new_coords = self.ui.get_coords()
                    SoldierMoveService(soldier=soldier, board=self.board, **new_coords).perform()
                elif action == Actions.FIGHT:
                    print('fighting')
                else:
                    raise AttributeError('Unknown action type')
                self.board.render()

    def game_finished(self):
        for player in self.players:
            if player.is_winner(self):
                self.winner = player
                return True
        return False

    def finish_game(self):
        self.ui.congratulate_winner(self.winner)
        self.ui.finish_game()
