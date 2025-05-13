from handlers import ILogHandler
from filters import ILogFilter


class Logger:
    def __init__(self, filters: list[ILogFilter], handlers: list[ILogHandler]) -> None:
        self._filters = filters
        self._handlers = handlers


    def log(self, text: str) -> None:
        if not any(filter_.match(text) for filter_ in self._filters):
            return

        for handler in self._handlers:
            handler.handle(text)
