import typing as t
from abc import ABC, abstractmethod


class IPropertyChangedListener(ABC):
    @abstractmethod
    def on_property_changed(self, obj: t.Any, property_name: str) -> None:
        pass


class MyPropertyChangedListener(IPropertyChangedListener):
    def __init__(self, phase: str = " Офигеть!") -> None:
        self._phase = phase

    def on_property_changed(self, obj: t.Any, property_name: str) -> None:
        print(f"Значение {property_name} изменилось у {obj}!{self._phase}")


class INotifyDataChanged(ABC):
    def add_property_changed_listener(self, listener: IPropertyChangedListener) -> None:
        pass

    def remove_property_changed_listener(self, listener: IPropertyChangedListener) -> None:
        pass


class MeowNotifyDataChanged(INotifyDataChanged):
    def __init__(self) -> None:
        self._listeners: list[IPropertyChangedListener] = []

        self._cat = "The cat"
        self._dog = 52

    def add_property_changed_listener(self, listener: IPropertyChangedListener) -> None:
        self._listeners.append(listener)

    def remove_property_changed_listener(self, listener: IPropertyChangedListener) -> None:
        self._listeners.remove(listener)

    @property
    def cat(self):
        return self._cat

    @cat.setter
    def cat(self, value: str):
        self._notify_listeners(property_name="cat")
        self._cat = value

    @property
    def dog(self):
        return self._dog

    @dog.setter
    def dog(self, value: int):
        self._notify_listeners(property_name="dog")
        self._dog = value

    def _notify_listeners(self, property_name: str) -> None:
        for listener in self._listeners:
            listener.on_property_changed(obj=self, property_name=property_name)
