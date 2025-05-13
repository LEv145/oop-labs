from memento import KeyboardStateSaver
from keyboard import Keyboard
from commands import ABCCommand, CharPrintCommand, VolumeUpCommand, VolumeDownCommand, MediaPlayerCommand


def main() -> None:
    supported_commands: list[ABCCommand] = [
        CharPrintCommand(char="a"),
        VolumeUpCommand(),
        VolumeDownCommand(),
        MediaPlayerCommand(),
    ]
    saver = KeyboardStateSaver("keyboard_state.json")

    print("== Конфигурация ==")
    keyboard = Keyboard(saver=saver, supported_commands=supported_commands)
    keyboard.add_hotkey("CTRL+A", "volume_up")
    keyboard.add_hotkey("CTRL+Z", "volume_down")
    keyboard.add_hotkey("A", "char_print_a")
    keyboard.add_hotkey("B", "char_print_a")
    keyboard.undo_add_hotkey()

    print("== Тестирование ==")
    keyboard.do("A")
    keyboard.do("A")
    keyboard.undo()
    keyboard.do("CTRL+A")
    keyboard.do("CTRL+Z")
    keyboard.undo()
    keyboard.redo()


if __name__ == "__main__":
    main()
