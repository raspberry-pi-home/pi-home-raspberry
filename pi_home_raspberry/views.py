import json
import logging
import uuid

from aiohttp.web import (
    View,
    WebSocketResponse,
    WSMsgType,
)
import aiohttp_jinja2
import ujson


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# TODO: does this make sense?
async def _notify_active_connections(websockets):

    # gather connections and send them to all websockets
    connections_data = {}
    connections_data['active_connections'] = len(websockets)
    connections_data = json.dumps(connections_data)
    for ws in websockets:
        await ws.send_str(connections_data)


async def _notify_app_changes(websockets, raspberry_app):

    # serialize app and send it to the websocket
    app_data = raspberry_app.to_json()
    for ws in websockets:
        await ws.send_str(app_data)


async def _websocket_message_handler(msg, ws_response, websockets, raspberry_app):
    logger.info('Got %s message from websocket', msg.data)

    # try to parse the message as json
    try:
        data = msg.json()
    except json.JSONDecodeError:
        logger.warning('Unable to parse websocket json message')

        # is message is not in a json format, we will do nothing
        return ws_response

    action, status = raspberry_app.process_message(data, ws_response)

    # TODO: do we need to do this on this app
    # respond with the status of the message
    ws_response.send_json({
        'action': '{action}_{status}'.format(
            action=action,
            status='ok' if bool(status) else 'not_ok',
        )
    })


class IndexView(View):

    @aiohttp_jinja2.template('index.html')
    async def get(self):
        raspberry_app = self.request.app['raspberry_app']

        return {
            'host_ip': raspberry_app.host_ip,
            'host_name': raspberry_app.host_name,
            'host_port': raspberry_app.host_port,
        }


class WebSocketView(View):

    async def get(self):
        request = self.request
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
            await _notify_app_changes(
                [ws_response],
                raspberry_app,
            )

            # notify about active connections
            await _notify_active_connections(websockets)

            # TODO: I couldn't make this work using .receive() method because
            # of the middlewares. So, again, does middlewares makes sense for this
            # project?
            async for msg in ws_response:
                # we only care about text messages
                if msg.type == WSMsgType.TEXT:
                    await _websocket_message_handler(
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
            await _notify_active_connections(websockets)
