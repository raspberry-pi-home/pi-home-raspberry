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
        pin = action['pin']
        status = action['status']

        self.board.change_pin_status(pin, status)

    def to_json(self):
        return json.dumps(self, cls=ObjectEncoder)
