import json
import logging

from aiohttp.web import (
    Response,
    WebSocketResponse,
    WSMsgType,
)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def index_handler(request):
    # TODO: this along with /static should serve frontend app
    return Response(text='Hello, world')


async def notify_active_connections(websockets):

    # gather connections and send them to all websockets
    connections_data = {}
    connections_data['active_connections'] = len(websockets)
    connections_data = json.dumps(connections_data)
    for ws in websockets:
        await ws.send_str(connections_data)


async def notify_app_changes(websockets, raspberry_app):

    # serialize app and send it to the websocket
    app_data = raspberry_app.to_json()
    for ws in websockets:
        await ws.send_str(app_data)


async def websocket_message_handler(msg, ws_response, websockets, raspberry_app):
    logger.info('Got %s message from websocket', msg.data)

    # try to parse the message as json
    try:
        data = msg.json()
    except json.JSONDecodeError:
        logger.warning('Unable to parse websocket json message')

        # is message is not in a json format, we will do nothing
        return

    should_notify_self, should_notify_others = raspberry_app.excecute_action(data)
    # notify changes in the raspberry app
    if should_notify_others:
        await notify_app_changes(
            websockets,
            raspberry_app,
        )
    elif should_notify_self:
        await notify_app_changes(
            [ws_response],
            raspberry_app,
        )


async def websocket_handler(request):
    ws_response = WebSocketResponse()
    ok, protocol = ws_response.can_prepare(request)
    if not ok:
        logger.info('Unable to prepare connection between server and websocket')
        return ws_response

    await ws_response.prepare(request)

    try:
        raspberry_app = request.app['raspberry_app']
        websockets = request.app['websockets']
        websockets.append(ws_response)

        logger.info('A new websocket is connected, total: %s', len(websockets))

        # notify changes in the raspberry app
        await notify_app_changes(
            [ws_response],
            raspberry_app,
        )

        # notify about active connections
        await notify_active_connections(websockets)

        # TODO: I couldn't make this work using .receive() method because
        # of the middlewares. So, again, does middlewares makes sense for this
        # project?
        async for msg in ws_response:
            # we only care about text messages
            if msg.type == WSMsgType.TEXT:
                await websocket_message_handler(
                    msg,
                    ws_response,
                    websockets,
                    raspberry_app,
                )

            else:
                return ws_response

        return ws_response

    finally:
        websockets = request.app['websockets']
        websockets.remove(ws_response)

        logger.info('A websocket is disconnected, total: %s', len(websockets))

        # notify about active connections
        await notify_active_connections(websockets)

routes = [
    ('GET', '/', index_handler),
    ('GET', '/ws', websocket_handler),
]
