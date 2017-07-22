import json
import logging
from socket import (
    AF_INET,
    SOCK_DGRAM,
    gethostname,
    socket,
)

from pi_home_raspberry.board import Board
from pi_home_raspberry.encoder import ObjectEncoder


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

    def process_message(self, message):
        if 'action' not in message:
            return False, False

        if 'data' not in message:
            return False, False

        action_key = 'action_{action_name}'.format(
            action_name=message['action'],
        )
        if not hasattr(self.board, action_key):
            return False, False

        data = message['data']
        method = getattr(self.board, action_key)
        return method(data)

    def to_json(self):
        return json.dumps(self, cls=ObjectEncoder)
