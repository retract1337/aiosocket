from aiosocket import Dispatcher

from .middlewares import (
    LoggingMiddleware,
    AuthenticationMiddleware,
    HmacValidationMiddleware,
)


def setup_middlewares(dp: Dispatcher) -> None:
    dp.include_middleware(LoggingMiddleware(), True)
    dp.include_middleware(LoggingMiddleware(), False)
    dp.include_middleware(AuthenticationMiddleware(), True)
    dp.include_middleware(HmacValidationMiddleware(), True)
    dp.include_middleware(HmacValidationMiddleware(), False)
