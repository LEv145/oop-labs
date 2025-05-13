import json
from pathlib import Path


class KeyboardMemento:
    def __init__(self, state: dict[str, str]):
        self._state = state

    def get_state(self) -> dict[str, str]:
        return self._state.copy()


class KeyboardStateSaver:
    def __init__(self, save_file: Path | str) -> None:
        self._save_file: Path = Path(save_file)

    def set_memento(self, memento: KeyboardMemento) -> None:
        with open(self._save_file, "w") as fp:
            json.dump(memento.get_state(), fp, ensure_ascii=False, indent=4)

    def create_memento(self) -> KeyboardMemento:
        if not self._save_file.exists():
            with open(self._save_file, "w") as fp:
                json.dump({}, fp, ensure_ascii=False, indent=4)

        with open(self._save_file) as fp:
            state = json.load(fp)

        return KeyboardMemento(state)

    def add_hotkey(self, hotkey: str, command: str) -> None:
        with open(self._save_file) as fp:
            state = json.load(fp)

        state[hotkey] = command

        with open(self._save_file, "w") as fp:
            json.dump(state, fp, ensure_ascii=False, indent=4)
