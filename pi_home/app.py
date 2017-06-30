import json
import logging
from socket import (
    AF_INET,
    SOCK_DGRAM,
    gethostname,
    socket,
)

from pi_home.board import Board
from pi_home.encoder import ObjectEncoder


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class App:

    def __init__(self, config, port):
        self._board = Board(config)
        self._port = port

    @property
    def board(self):
        return self._board

    @property
    def host_ip(self):
        my_ip = '127.0.0.1'
        try:
            fake_socket = socket(AF_INET, SOCK_DGRAM)
            fake_socket.connect(('8.8.8.8', 80))
            my_ip = fake_socket.getsockname()[0]
            fake_socket.close()
        except Exception:
            logger.warning('Unable to get host ip address')
            pass

        return my_ip

    @property
    def host_name(self):
        return gethostname()

    @property
    def host_port(self):
        return self._port

    def excecute_action(self, action):
        # first return value is if we have to notify ourselves about the changes
        # second return value is if we have to notify others about the changes
        # errors means no notifying
        if 'set_value' in action:
            errors = []
            for key, value in action['set_value'].items():
                if not self.board.set_pin_value(key, value):
                    errors.append(0)

            return False, not len(errors)

        # TODO: implement other cases

    def to_json(self):
        return json.dumps(self, cls=ObjectEncoder)
