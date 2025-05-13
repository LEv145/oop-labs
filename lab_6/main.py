from abc import ABC, abstractmethod


class ABCCommand(ABC):
    def do(self) -> None:
        pass

    def undo(self) -> None:
        pass


class CharPrintCommand(ABCCommand):
    def __init__(self, char: str) -> None:
        self.char = char

    def do(self) -> None:
        print(self.char, end="")

    def undo(self) -> None:
        print(f"\r{self.char}", end="")


class VolumeUpCommand(ABCCommand):
    def __init__(self) -> None:
        self.volume = 50

    def do(self) -> None:
        self.volume = min(100, self.volume + 20)

    def undo(self) -> None:
        self.volume = max(0, self.volume - 20)



class VolumeDownCommand(ABCCommand):
    def __init__(self) -> None:
        self.volume = 50

    def do(self) -> None:
        self.volume = max(0, self.volume - 20)

    def undo(self) -> None:
        self.volume = min(100, self.volume + 20)


class MediaPlayerCommand(ABCCommand):
    def __init__(self) -> None:
        self.player_on = False

    def do(self) -> None:
        if not self.player_on:
            self.player_on = True

    def undo(self) -> None:
        if self.player_on:
            self.player_on = False
