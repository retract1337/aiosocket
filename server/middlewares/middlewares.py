import asyncio

from aiosocket.models import RequestModel, Session
from aiosocket.models.middleware import BaseMiddleware
from aiosocket.utilities import validate_message

from loguru import logger
from typing import Callable


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
        Логирование всех запросов клиента

        :param session: Сессия
        :param reader: Сокет для чтения
        :param writer: Сокет для записи
        :param request_data: Данные запроса
        :param handler: Хендлер, если требуется
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


class AuthenticationMiddleware(BaseMiddleware):
    async def process(
        self,
        session: Session,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        request_data: RequestModel,
        handler: Callable[..., None],
    ) -> None:
        """
        Проверка на авторизацию

        :param session: Сессия
        :param reader: Сокет для чтения
        :param writer: Сокет для записи
        :param request_data: Данные запроса
        :param handler: Хендлер, если требуется
        """

        if session.authorized:
            await super().process(
                session=session,
                reader=reader,
                writer=writer,
                request_data=request_data,
                handler=handler,
            )
        else:
            await self.send_response(
                writer,
                status=False,
                message="Stupid monki",
                type="unauthorized",
            )


class HmacValidationMiddleware(BaseMiddleware):
    async def process(
        self,
        session: Session,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        request_data: RequestModel,
        handler: Callable[..., None],
    ) -> None:
        """
        Валидация HMAC в запросе

        :param session: Сессия
        :param reader: Сокет для чтения
        :param writer: Сокет для записи
        :param request_data: Данные запроса
        :param handler: Хендлер, если требуется
        """

        if self.validate_message(request_data):
            await super().process(
                session=session,
                reader=reader,
                writer=writer,
                request_data=request_data,
                handler=handler,
            )
        else:
            await self.send_response(
                writer,
                status=False,
                message="Invalid HMAC.",
                type="invalid_hmac",
            )

    def validate_message(self, request_data: RequestModel) -> bool:
        """
        Валидация сообщения

        :param request_data: Данные запроса
        :return: True если валидно, иначе False
        """

        message_dict = request_data.model_dump()
        return validate_message("secret_key".encode(), message_dict, 5)
