from abc import ABC, abstractmethod


_computer_volume = 50


class ABCCommand(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def do(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass


class CharPrintCommand(ABCCommand):
    def __init__(self, char: str) -> None:
        self.char = char

    def get_name(self) -> str:
        return f"char_print_{self.char}"

    def do(self) -> None:
        print(f"✅ Напечатан символ `{self.char}`")

    def undo(self) -> None:
        print(f"⏮️ Откат печати символа `{self.char}`")


class VolumeUpCommand(ABCCommand):
    def get_name(self) -> str:
        return "volume_up"

    def do(self) -> None:
        global _computer_volume
        last_volume = _computer_volume
        _computer_volume = min(100, _computer_volume + 20)
        print(f"✅ Увеличена громкость громкость: {last_volume} -> {_computer_volume}")

    def undo(self) -> None:
        global _computer_volume
        last_volume = _computer_volume
        _computer_volume = max(0, _computer_volume - 20)
        print(f"⏮️ Откат увеличения громкости: {last_volume} -> {_computer_volume}")


class VolumeDownCommand(ABCCommand):
    def __init__(self) -> None:
        self.volume = 50

    def get_name(self) -> str:
        return "volume_down"

    def do(self) -> None:
        global _computer_volume
        last_volume = _computer_volume
        _computer_volume = max(0, _computer_volume - 20)
        print(f"✅ Уменьшена громкость громкость: {last_volume} -> {_computer_volume}")

    def undo(self) -> None:
        global _computer_volume
        last_volume = _computer_volume
        _computer_volume = min(100, _computer_volume + 20)
        print(f"⏮️ Откат уменьшения громкости: {last_volume} -> {_computer_volume}")


class MediaPlayerCommand(ABCCommand):
    def __init__(self) -> None:
        self.player_on = False

    def get_name(self) -> str:
        return "media_player"

    def do(self) -> None:
        if not self.player_on:
            self.player_on = True
        print(f"✅ Открыт плеер")

    def undo(self) -> None:
        if self.player_on:
            self.player_on = False
        print(f"⏮️ Откат открытия плеера плеер")
