import typing as t
from abc import ABC, abstractmethod


class ILogFilter(ABC):
    @abstractmethod
    def match(self, text: str) -> bool:
        pass


class TextLogFilter(ILogFilter):
    def __init__(self, pattern: str) -> None:
        self._pattern = pattern

    def match(self, text: str) -> bool:
        return self._pattern in text


class RegexLogFilter(ILogFilter):
    def __init__(self, pattern: t.Pattern) -> None:
        self._pattern = pattern

    def match(self, text: str) -> bool:
        return self._pattern.search(text) is not None
