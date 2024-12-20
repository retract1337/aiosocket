import asyncio

from aiosocket.models import RequestModel, Session
from aiosocket.models.handler import BaseHandler


class PingHandler(BaseHandler):
    async def handle(
        self,
        session: Session,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        request_data: RequestModel,
    ) -> None:
        """
        Пинг клиента

        :param session: Сессия
        :param reader: Сокет для чтения
        :param writer: Сокет для записи
        :param request_data: Данные запроса
        """

        response_message = "Pong!\n"
        writer.write(response_message.encode())
        await writer.drain()


class AnotherHandler(BaseHandler):
    async def handle(
        self,
        session: Session,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        request_data: RequestModel,
    ) -> None:
        response_message = (
            f"WTH ARE U TALKIN NIGGA SHUT UR BITCH ASS: {request_data.type}\n"
        )

        writer.write(response_message.encode())
        await writer.drain()
