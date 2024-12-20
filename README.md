# ⏲️ AioSocket
An asynchronous library for asyncio sockets.

Actually, it's just an old build of my project, so I think it might be a good idea to post this here...

## TODO
- Rewrite the middleware system (it's shitty af).
- Rewrite the structure.
- Fix typings, cuz those are ass.

### Examples
```python3
import asyncio
from loguru import logger
from typing import Callable
from server.handlers import setup_handlers
from server.middlewares import setup_middlewares
from aiosocket import Dispatcher, Server
from aiosocket.models import RequestModel, Session, CustomSession
from aiosocket.models.handler import BaseHandler
from aiosocket.models.middleware import BaseMiddleware
class LoggingMiddleware(BaseMiddleware):
    async def process(
        self,
        session: Session,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        request_data: RequestModel,
        handler: Callable[..., None],
    ) -> None:
        """
        basic logger
        """
        logger.info(
            f"Received request: {request_data}",
        )
        await super().process(
            session=session,
            reader=reader,
            writer=writer,
            request_data=request_data,
            handler=handler,
        )
class LoginHandler(BaseHandler):
    async def handle(
        self,
        session: Session,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        request_data: RequestModel,
    ) -> None:
        """
        auth handler
        """
        if self.authenticate(request_data):
            session.authorize(
                request_data.data["username"],
            )
            self.send_response(
                writer,
                status=True,
                message="Authentication successful",
                data={"username": session.username},
                type="authorized",
            )
        else:
            self.send_response(
                writer,
                status=False,
                message="Failed, lil bro",
                type="auth_failed",
            )
    def authenticate(self, request_data: RequestModel) -> bool:
        """
        auth check
        """
        return request_data.data.get("username") == "admin"
class AnotherHandler(BaseHandler):
    async def handle(self, session, reader, writer, request_data):
        response_message = "Another handler response"
        writer.write(response_message.encode())
        await writer.drain()
async def main() -> None:
    dispatcher = Dispatcher(session_class=CustomSession)
    server = Server(host="127.0.0.1", port=8888, dispatcher=dispatcher)
    user_router = server.dispatcher.create_router("user")
    user_router.add_handler(AnotherHandler(), name="another_handler")
    user_router.add_middleware(LoggingMiddleware())
    test_router = server.dispatcher.create_router("test")
    test_router.add_handler(LoginHandler(), name="login_handler")
    await server.run_server()
if __name__ == "__main__":
    asyncio.run(main())
```

