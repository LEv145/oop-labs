from memento import KeyboardStateSaver
from commands import ABCCommand


class Keyboard():
    def __init__(self, saver: KeyboardStateSaver) -> None:
        self._saver = saver

        self._history = []

    def add_hotkey(self, hotkey: str, command: ABCCommand) -> None:
