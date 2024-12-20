import asyncio

from aiosocket.models import RequestModel, Session
from aiosocket.models.handler import BaseHandler


class LoginHandler(BaseHandler):
    async def handle(
        self,
        session: Session,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        request_data: RequestModel,
    ) -> None:
        """
        Авторизация клиента

        :param session: Сессия
        :param reader: Сокет для чтения
        :param writer: Сокет для записи
        :param request_data: Данные запроса
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
        Проверяет пользователя на авторизацию

        :param request_data: Данные запроса
        """

        return request_data.data.get("username") == "admin"
