from pi_home_raspberry.views import (
    IndexView,
    WebSocketView,
)


routes = [
    ('GET', '/', IndexView),
    ('GET', '/ws', WebSocketView),
]
