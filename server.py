import asyncio
import json
import logging
import os
import sys

from aiohttp.web import (
    Application,
    HTTPException,
    Response,
    WebSocketResponse,
    WSMsgType,
)

from app import App
from config import get_config


logging.basicConfig(
    format='%(asctime)s:%(name)s:%(pathname)s:%(levelname)s: %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S%z',
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

STATIC_FOLDER = os.path.join(os.path.dirname(__file__), './static')


def json_error(message, status):
    logger.warning('Web server error: http=%s error=%s', status, message)
    return Response(
        status=status,
        text='There was an error executing your request',
    )


# TODO: does this makes sense on a websocket
async def error_middleware(web_app, handler):
    async def middleware_handler(request):
        try:
            response = await handler(request)
            # TODO: ?
            # we don't care about WebSocketResponse (for now)
            if isinstance(response, WebSocketResponse):
                return response
            if response.status == 200:
                return response
            return json_error(response.message, response.status)
        except HTTPException as ex:
            if ex.status != 200:
                return json_error(ex.reason, ex.status)
            raise
    return middleware_handler


async def index_handler(request):
    # TODO: change this
    return Response(text='Hello, world')


# TODO: improve this
async def websocket_handler(request):
    ws_response = WebSocketResponse()
    ok, protocol = ws_response.can_prepare(request)
    if not ok:
        # TODO: do something (?)
        pass

    await ws_response.prepare(request)

    try:
        print('Someone joined')
        for ws in request.app['websockets']:
            await ws.send_str('Someone joined')

        request.app['websockets'].append(ws_response)

        async for msg in ws_response:
            if msg.type == WSMsgType.TEXT:
                # try to parse the message as json
                try:
                    data = msg.json()
                except json.decoder.JSONDecodeError:
                    logger.warning('Unable to parse websocket json message')
                    # fallback and treat the message as string
                    data = msg.data

                # TODO: this will likely change since we will receive allways json messages
                string_data = data
                if type(string_data) == dict:
                    string_data = json.dumps(string_data)

                await ws_response.send_str(string_data + '/answer')

                for ws in request.app['websockets']:
                    if ws is not ws_response:
                        await ws.send_str(string_data)

            else:
                return ws_response

        return ws_response

    finally:
        request.app['websockets'].remove(ws_response)
        print('Someone disconnected')
        for ws in request.app['websockets']:
            await ws.send_str('Someone disconnected')


async def init(loop):
    logger.info('Building configuration')
    config = get_config()
    if not config:
        logger.info('Applicaion terminated')
        sys.exit()

    logger.info('App configuration: %s', config)

    logger.info('Building application')
    raspberry_app = App(config)

    logger.info('Building web application')
    web_app = Application(
        loop=loop,
        middlewares=[
            error_middleware,
        ],
    )
    web_app['websockets'] = []
    web_app['raspberry_app'] = raspberry_app

    web_app.router.add_get('/', index_handler)
    web_app.router.add_get('/ws', websocket_handler)
    web_app.router.add_static('/static', STATIC_FOLDER)

    web_app.on_shutdown.append(on_shutdown)

    logger.info('Starting web server')
    web_app_handler = web_app.make_handler()
    server_generator = loop.create_server(
        web_app_handler,
        host='0.0.0.0',
        port=8000,
    )

    return server_generator, web_app_handler, web_app


async def on_shutdown(web_app):
    for ws in web_app['websockets']:
        await ws.close(code=1001, message='Server shutdown')


async def shutdown(server, web_app, web_app_handler):
    logger.info('Stopping main server')
    server.close()
    await server.wait_closed()
    logger.info('Stopping web application')
    await web_app.shutdown()
    await web_app_handler.finish_connections(10.0)
    await web_app.cleanup()


if __name__ == '__main__':
    logger.info('Starting application')

    loop = asyncio.get_event_loop()
    server_generator, web_app_handler, web_app = loop.run_until_complete(init(loop))
    server = loop.run_until_complete(server_generator)

    logger.info('Starting web server: %s', str(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info('Stopping application')
    finally:
        loop.run_until_complete(shutdown(server, web_app, web_app_handler))
        loop.close()

    logger.info('Applicaion stopped')
