import typing as t
from abc import ABC, abstractmethod


class IPropertyChangingListener(ABC):
    @abstractmethod
    def on_property_changing(self, obj: t.Any, property_name: str, old_value: t.Any, new_value: t.Any) -> bool:
        pass


class MyPropertyChangingListener(IPropertyChangingListener):
    def on_property_changing(self, obj: t.Any, property_name: str, old_value: t.Any, new_value: t.Any) -> bool:
        return new_value > old_value


class INotifyDataChanging(ABC):
    def add_property_changing_listener(self, listener: IPropertyChangingListener) -> None:
        pass

    def remove_property_changing_listener(self, listener: IPropertyChangingListener) -> None:
        pass


class MeowNotifyDataChanging(INotifyDataChanging):
    def __init__(self) -> None:
        self._listeners: list[IPropertyChangingListener] = []

        self._cat = "The cat"
        self._dog = 52

    def add_property_changed_listener(self, listener: IPropertyChangingListener) -> None:
        self._listeners.append(listener)

    def remove_property_changed_listener(self, listener: IPropertyChangingListener) -> None:
        self._listeners.remove(listener)

    @property
    def cat(self):
        return self._cat

    @cat.setter
    def cat(self, value: str):
        self._cat = self._validate_or_change(property_name="cat", old_value=self._cat, new_value=value)

    @property
    def dog(self):
        return self._dog

    @dog.setter
    def dog(self, value: int):
        self._dog = self._validate_or_change(property_name="dog", old_value=self._dog, new_value=value)

    def _validate_or_change(self, property_name: str, old_value: t.Any, new_value: t.Any) -> bool:
        if all(
            listener.on_property_changing(
                obj=self,
                property_name=property_name,
                old_value=old_value,
                new_value=new_value,
            )
            for listener in self._listeners
        ):
            return new_value
        return old_value
