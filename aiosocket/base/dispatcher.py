import asyncio
import uuid
import pydantic

from typing import Optional, Type
from loguru import logger

from aiosocket.models import RequestModel, Session
from aiosocket.models.router import BaseRouter as Router
from aiosocket.models.storage import BaseStorage

from aiosocket.enums import Responses, ServerResponses
from aiosocket.utilities import ResponseBuilder
from aiosocket.base.storage import SessionsStorage


class RoutersStorage(BaseStorage[Router]):
    """
    Basic implementation of the routers storage
    """

    pass


class Dispatcher:
    """Dispatcher for handling client requests"""

    def __init__(self, session_class: Type[Session] = Session) -> None:
        """
        Dispatcher constructor

        :param session_class: Class used for session creation (default: Session)
        """

        self.sessions = SessionsStorage()
        self.routers = RoutersStorage()
        self.session_class = session_class

    def create_router(self, name: str) -> Router:
        """
        Creates a new router and registers it

        :param name: Name of the router
        :return: Router instance
        """

        if name in self.routers:
            raise ValueError(f"Router with name '{name}' already exists.")

        router = Router()
        self.routers.add(name, router)
        return router

    def find_router(self, handler_name: str) -> Optional[str]:
        """
        Finds the router name by searching for a handler within all routers.

        :param handler_name: Name of the handler to search for
        :return: Router name if found, otherwise None
        """

        for router_name, router in self.routers._storage.items():
            try:
                if router.get_handler(handler_name):
                    return router_name
            except Exception:
                continue
        return None

    async def dispatch(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        """
        Main method of the dispatcher for handling client requests

        :param reader: Stream reader
        :param writer: Stream writer
        """

        session_id = str(uuid.uuid4())
        peername = writer.get_extra_info("peername")
        session = self.session_class(session_id=session_id, peername=str(peername))
        self.sessions.add(session_id, session)

        logger.debug(
            f"New connection -> {session_id} | {peername}",
        )

        while True:
            data = await reader.read(1024)
            if not data:
                logger.debug(f"{session_id} -> Connection closed")
                break

            try:
                message = data.decode()
                print(message)

                request_data = RequestModel.model_validate_json(message)
                handler_name = request_data.type.lower()
                router_name = self.find_router(handler_name)

                logger.debug(f"{session_id} -> Received request: {message}")

                if router_name:
                    router = self.routers.get(router_name)
                    handler = router.get_handler(handler_name)

                    if handler:
                        await router.apply_middlewares(
                            session,
                            reader,
                            writer,
                            request_data,
                            handler.handle,
                        )
                    else:
                        self.send_response(
                            writer,
                            status=False,
                            message=Responses.ERROR.value,
                            data={"error": ServerResponses.NOT_FOUND.value},
                        )
                        await writer.drain()
                else:
                    self.send_response(
                        writer,
                        status=False,
                        message=Responses.ERROR.value,
                        data={"error": ServerResponses.NOT_FOUND.value},
                    )
                    await writer.drain()

            except pydantic.ValidationError as error:
                logger.error(
                    f"{session_id} -> Validation error: {error}",
                )

                self.send_response(
                    writer,
                    status=False,
                    message=Responses.ERROR.value,
                    data={
                        "error": ServerResponses.ERROR.value,
                        "details": str(error),
                    },
                )
                await writer.drain()

            except Exception as error:
                logger.error(f"{session_id} -> Error while processing request {error}")
                self.send_response(
                    writer,
                    status=False,
                    message=Responses.ERROR.value,
                    data={"error": ServerResponses.INTERNAL_ERROR.value},
                )
                await writer.drain()

        writer.close()
        await writer.wait_closed()
        self.sessions.remove(session_id)

    def send_response(
        self,
        writer: asyncio.StreamWriter,
        status: bool,
        message: str,
        data: dict = None,
        type: str = "response",
    ) -> None:
        """
        Sends response to the client

        :param writer: Stream writer
        :param status: Status of the response
        :param message: Message of the response
        :param data: Data of the response
        :param type: Type of the response
        """

        response_message = ResponseBuilder(
            status=status, message=message, data=data, type=type
        ).build()
        writer.write(response_message.model_dump_json().encode())
