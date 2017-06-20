import asyncio
import logging
import sys

import aiohttp
from aiohttp import web

from app import App
from config import get_config


logging.basicConfig(format='%(asctime)s:%(name)s:%(pathname)s:%(levelname)s: %(message)s', datefmt='%Y-%m-%dT%H:%M:%S%z')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def index_handler(request):
    return web.Response(text='Hello, world')


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app['websockets'].append(ws)

    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    await ws.send_str(msg.data + '/answer')
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('websocket connection closed with exception %s', ws.exception())
    finally:
        request.app['websockets'].remove(ws)

    print('websocket connection closed')

    return ws


async def on_shutdown(web_app):
    for ws in web_app['websockets']:
        await ws.close(code=1001, message='Server shutdown')


async def shutdown(server, web_app, handler):
    logger.info('Stopping main server')
    server.close()
    await server.wait_closed()
    logger.info('Stopping web application')
    await web_app.shutdown()
    await handler.finish_connections(10.0)
    await web_app.cleanup()


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
    web_app = web.Application(loop=loop)
    web_app['websockets'] = []
    web_app['raspberry_app'] = raspberry_app

    web_app.router.add_get('/', index_handler)
    web_app.router.add_get('/ws', websocket_handler)
    web_app.router.add_static('/static', './static')

    web_app.on_shutdown.append(on_shutdown)

    logger.info('Starting web server')
    handler = web_app.make_handler()
    server_generator = loop.create_server(
        handler,
        host='0.0.0.0',
        port=8000,
    )

    return server_generator, handler, web_app


if __name__ == '__main__':
    logger.info('Starting application')

    loop = asyncio.get_event_loop()
    server_generator, handler, web_app = loop.run_until_complete(init(loop))
    server = loop.run_until_complete(server_generator)

    logger.info('Starting web server: %s', str(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info('Stopping application')
    finally:
        loop.run_until_complete(shutdown(server, web_app, handler))
        loop.close()

    logger.info('Applicaion stopped')
