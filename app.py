from board import Board


class App:

    def __init__(self, config):
        self._board = Board(config)

    def excecute_action(self, action):
        pin = action['pin']
        status = action['status']

        self._board.change_pin_status(pin, status)

    def get_board_status(self):
        # TODO: instead of returning this, we should serialize the board and
        # serialize pins
        return self._board.get_pin_status()