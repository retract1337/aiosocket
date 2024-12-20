from .base import PingHandler, AnotherHandler
from .login import LoginHandler

from aiosocket import Dispatcher


def setup_handlers(dp: Dispatcher) -> None:
    dp.include_handlers(
        [
            LoginHandler,
            AnotherHandler,
        ],
        is_protected=False,
    )

    dp.include_handler(
        PingHandler,
        is_protected=True,
        name="another_handler",
    )
