from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, ChannelNameRouter, URLRouter

from apps.accounts.consumers import AccountBackgroundTasks
from apps.chats import routing

application = ProtocolTypeRouter({
    'channel': ChannelNameRouter({
        "accounts": AccountBackgroundTasks,
    }),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
