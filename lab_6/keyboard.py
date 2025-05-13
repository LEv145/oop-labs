from memento import KeyboardStateSaver, KeyboardMemento
from commands import ABCCommand


class Keyboard:
    def __init__(self, saver: KeyboardStateSaver, supported_commands: list[ABCCommand]) -> None:
        self._saver = saver
        self._supported_commands = supported_commands

        self._keyboard_states: list[KeyboardMemento] = []
        self._history: list[ABCCommand] = []

    def add_hotkey(self, hotkey: str, string_command: str) -> None:
        self._keyboard_states.append(self._saver.create_memento())
        command = self._get_command(string_command)
        self._saver.add_hotkey(hotkey, command.get_name())

    def undo_add_hotkey(self) -> None:
        if len(self._keyboard_states) == 1:
            self._saver.set_memento(self._keyboard_states[0])
        else:
            state = self._keyboard_states.pop()
            self._saver.set_memento(state)

    def do(self, key: str) -> None:
        state = self._saver.create_memento().get_state()
        for bind_key, string_command in state.items():
            if bind_key == key:
                command = self._get_command(string_command)
                command.do()
                self._history.append(command)

    def undo(self) -> None:
        if not self._history:
            return

        last_command = self._history.pop()
        last_command.undo()

    def redo(self) -> None:
        if not self._history:
            return

        last_command = self._history[-1]
        last_command.undo()
        last_command.do()

    def _get_command(self, string_command: str) -> ABCCommand:
        for command in self._supported_commands:
            if string_command == command.get_name():
                return command
        raise RuntimeError(f"Command {string_command} not found")
