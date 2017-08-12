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

    def process_message(self, message, client):
        action_name = message.get('action')
        if not action_name:
            return None, False

        data = message.get('data')
        if not data:
            return action_name, False

        action_key = 'action_{action_name}'.format(
            action_name=action_name,
        )
        method = getattr(self, action_key, None)
        if not method:
            return action_name, False

        logger.info('Processing \'%s\' action', action_name)
        success = False
        try:
            success = method(action_name, data, message, client)
        except Exception as e:
            logger.error('There was an error excecuting \'%s\'. Error: %s', action_name, e)
            pass

        logger.info('Action \'%s\' end %s', action_name, 'successfully' if success else 'with failure')
        return action_name, success

    def action_set_value(self, action, data, message, client):
        success = self.board.set_value(data)

        if success:
            return self.action_get_board_status(action, data, message, client)

        return success

    def action_get_board_status(self, action, data, message, client):
        client.send_json({
            'action': 'board_status',
            'data': self.to_json(),
        })

        return True

    def to_json(self):
        return json.dumps(self, cls=ObjectEncoder)
