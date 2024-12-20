import asyncio

from loguru import logger
from .dispatcher import Dispatcher


class Server:
    """
    Base implementation of the socket server using asyncio

    :param host: Server host
    :param port: Server port
    :param dispatcher: Dispatcher instance
    """

    def __init__(
        self,
        host: str,
        port: int,
        dispatcher: Dispatcher = Dispatcher(),
    ) -> None:
        """
        Server constructor

        :param host: Server host
        :param port: Server port
        :param dispatcher: Dispatcher instance
        """

        self.host: str = host
        self.port: int = port
        self.dispatcher = dispatcher

    async def handle_connection(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        """
        Handles new connection and passes it to the dispatcher
        """

        await self.dispatcher.dispatch(reader, writer)

    async def run_server(self) -> None:
        """
        Run the server
        """

        server = await asyncio.start_server(
            self.handle_connection, self.host, self.port
        )

        addr = server.sockets[0].getsockname()
        logger.debug("Server started on {}:{}...".format(addr[0], addr[1]))

        async with server:
            await server.serve_forever()
