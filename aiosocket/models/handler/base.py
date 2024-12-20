import asyncio

from aiosocket.utilities import ResponseBuilder
from aiosocket.models import RequestModel, Session


class BaseHandler:
    async def handle(
        self,
        session: Session,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        request_data: RequestModel,
    ) -> None:
        raise NotImplementedError("Method 'handle' must be implemented")

    def send_response(
        self,
        writer: asyncio.StreamWriter,
        status: bool,
        message: str,
        data: dict = {},
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
