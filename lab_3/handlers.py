from pathlib import Path
from datetime import datetime
from abc import ABC, abstractmethod
from socket import socket, AF_INET, SOCK_DGRAM
from syslog import syslog


class ILogHandler(ABC):
    @abstractmethod
    def handle(self, text: str) -> None:
        pass


class ConsoleHandler(ILogHandler):
    def handle(self, text: str) -> None:
        print(_get_log_string(text))


class FileHandler(ILogHandler):
    def __init__(self, path: Path | str) -> None:
        self._path = Path(path)

    def handle(self, text: str) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("a", encoding="utf‑8") as fp:
            fp.write(_get_log_string(text))


class SocketHandler(ILogHandler):
    def __init__(self, host: str = "localhost", port: int = 514) -> None:
        self._address = (host, port)
        self._sock = socket(AF_INET, SOCK_DGRAM)

    def handle(self, text: str) -> None:
        self._sock.sendto(_get_log_string(text).encode(), self._address)


class SyslogHandler(ILogHandler):
    def handle(self, text: str) -> None:
        syslog(_get_log_string(text))


def _get_log_string(text: str) -> str:
    ts = datetime.now().isoformat(timespec="seconds")
    return f"[{ts}] {text}"
