import asyncio
import logging
import sys


import aiohttp
from aiohttp.web import WSMsgType

from pi_home_raspberry.app import App
from pi_home_raspberry.config import get_config


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def _websocket_message_handler(msg, ws_response, raspberry_app):
    logger.info('Got %s message from server', msg.data)

    # try to parse the message as json
    try:
        data = msg.json()
    except json.JSONDecodeError:
        logger.warning('Unable to parse websocket json message')

        # is message is not in a json format, we will do nothing
        return ws_response

    action, status = raspberry_app.process_message(data, ws_response)

    # respond with the status of the message
    # ws_response.send_json({
    #     'action': '{action}_{status}'.format(
    #         action=action,
    #         status='ok' if bool(status) else 'not_ok',
    #     )
    # })


async def init_server(loop):
    logger.info('Building configuration')
    config = get_config()
    if not config:
        logger.info('Application terminated')
        sys.exit()

    logger.info('App configuration: %s', config)

    host = config['app_settings']['host']
    port = config['app_settings']['port']

    logger.info('Building application')
    raspberry_app = App(config, port)

    ws_server_url = config['app_settings']['ws_server_url']
    auth_token = config['app_settings']['auth_token']

    session = aiohttp.ClientSession()
    while True:
        logger.info('Trying to connect to websocket server')
        try:
            async with session.ws_connect(ws_server_url) as ws_response:
                logger.info('Connected to websocket server')

                logger.info('Autheticating against websocket server')
                ws_response.send_json({
                    'action': 'connect',
                    'data': {
                        'auth_token': auth_token,
                        'role': 'raspberry',
                    },
                })

                async for msg in ws_response:
                    # we only care about text messages
                    if msg.type == WSMsgType.TEXT:
                        await _websocket_message_handler(
                            msg,
                            ws_response,
                            raspberry_app,
                        )
        except Exception as e:
            logger.info('Disconnected from websocket server')
            # wait 5 seconds before retry
            await asyncio.sleep(5)


def main():
    logger.info('Starting application')

    loop = asyncio.get_event_loop()
    server_generator = init_server(loop)
    loop.run_until_complete(server_generator)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info('Stopping application')
    finally:
        loop.close()

    logger.info('Application stopped')
