import asyncio
from typing import Callable

from aiosocket.models.sessions import Session
from aiosocket.models import RequestModel

from aiosocket.models.handler import BaseHandler
from aiosocket.models.middleware import BaseMiddleware
from aiosocket.base.storage import HandlersStorage, MiddlewaresStorage


class BaseRouter:
    """BaseRouter for managing handlers and middlewares"""

    def __init__(self) -> None:
        self._handlers = HandlersStorage()
        self._middlewares = MiddlewaresStorage()

    def add_handler(self, handler: BaseHandler, name: str = None) -> None:
        """
        Adds a handler to the router.

        :param handler: Handler to add
        :param name: Optional name of the handler
        """

        if name is None:
            name = handler.__class__.__name__.lower()
        self._handlers.add(name, handler)

    def add_middleware(self, middleware: BaseMiddleware, name: str = None) -> None:
        """
        Adds middleware to the router.

        :param middleware: Middleware to add
        :param name: Optional name of the middleware
        """

        if name is None:
            name = middleware.__class__.__name__.lower()
        self._middlewares.add(name, middleware)

    def get_handler(self, name: str) -> BaseHandler:
        """
        Retrieves a handler by name.

        :param name: Name of the handler
        :return: Handler instance
        """

        return self._handlers.get(name)

    def get_middlewares(self) -> MiddlewaresStorage:
        """
        Retrieves all middlewares.

        :return: MiddlewaresStorage instance
        """

        return self._middlewares

    async def apply_middlewares(
        self,
        session: "Session",
        reader: "asyncio.StreamReader",
        writer: "asyncio.StreamWriter",
        request_data: "RequestModel",
        handler: "Callable[..., None]",
    ) -> None:
        """Apply middlewares to the handler"""

        async def process_middlewares(
            index: int,
            session: "Session",
            reader: "asyncio.StreamReader",
            writer: "asyncio.StreamWriter",
            request_data: "RequestModel",
        ) -> None:
            """
            Processes middlewares recursively
            """

            if index < len(self._middlewares):
                middleware = list(self._middlewares._storage.values())[index]
                await middleware.process(
                    session=session,
                    reader=reader,
                    writer=writer,
                    request_data=request_data,
                    handler=lambda s, r, w, d: process_middlewares(
                        index + 1, s, r, w, d
                    ),
                )
            else:
                await handler(session, reader, writer, request_data)

        await process_middlewares(0, session, reader, writer, request_data)
