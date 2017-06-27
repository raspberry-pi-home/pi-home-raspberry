import json

from board import Board
from encoder import ObjectEncoder


class App:

    def __init__(self, config):
        self._board = Board(config)

    @property
    def board(self):
        return self._board

    def excecute_action(self, action):
        if 'set_value' in action:
            for key, value in action['set_value'].items():
                self.board.set_pin_value(key, value)
                break

            return False, True

        # TODO: implement other cases

    def to_json(self):
        return json.dumps(self, cls=ObjectEncoder)
