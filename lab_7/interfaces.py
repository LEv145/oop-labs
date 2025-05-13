from pathlib import Path
from abc import ABC, abstractmethod


class ILogger(ABC):
    @abstractmethod
    def log(self, msg: str) -> None:
        pass


class IFetcher(ABC):
    @abstractmethod
    def fetch(self) -> str:
        pass


class IService(ABC):
    @abstractmethod
    def run(self) -> None:
        pass


class ConsoleLogger(ILogger):
    def log(self, message: str) -> None:
        print(f"[console] {message}")


class FileLogger(ILogger):
    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)

    def log(self, message: str) -> None:
        with open(self._path, "a", encoding="utf‑8") as f:
            f.write(f"{message}\n")


class MemoryFetcher(IFetcher):
    def fetch(self) -> str:
        return "alpha, beta, gamma"


class SqlFetcher(IFetcher):
    def fetch(self) -> str:
        return "rows 1‑3 from DB"


class DebugService(IService):
    def __init__(self, logger: ILogger, fetcher: IFetcher) -> None:
        self._logger = logger
        self._fetcher = fetcher

    def run(self) -> None:
        self._logger.log(f"[DEBUG] {self._fetcher.fetch()}")


class ReleaseService(IService):
    def __init__(self, logger: ILogger, fetcher: IFetcher) -> None:
        self._logger = logger
        self._fetcher = fetcher

    def run(self) -> None:
        self._logger.log(f"[RELEASE] {self._fetcher.fetch()}")
