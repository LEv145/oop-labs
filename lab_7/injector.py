import typing as t
from enum import Enum, auto
from contextlib import contextmanager


T = t.TypeVar("T")


class LifeStyle(Enum):
    PER_REQUEST = auto()
    SCOPED = auto()
    SINGLETON = auto()


class _Registration:
    def __init__(
        self,
        provider: t.Callable[..., t.Any] | type[t.Any],  # Класс или фабрика
        lifestyle: LifeStyle,
        params: dict[str, t.Any] | None,
    ) -> None:
        self.provider = provider
        self.lifestyle = lifestyle
        self.params = params or {}


class Injector:
    def __init__(self) -> None:
        self._registrations: dict[type[t.Any], _Registration] = {}
        self._singletons: dict[type[t.Any], t.Any] = {}
        self._scope_stack: list[dict[type[t.Any], t.Any]] = []

    def register(
        self,
        interface: type[T],
        provider: t.Callable[..., T] | type[T],
        lifestyle: LifeStyle = LifeStyle.PER_REQUEST,
        params: dict[str, t.Any] | None = None,
    ) -> None:
        self._registrations[interface] = _Registration(provider, lifestyle, params)

    def get_instance(self, interface: type[T]) -> T:
        registration = self._registrations.get(interface)
        if registration is None:
            raise KeyError(f"Interface {interface} is not registration.")

        # Singleton
        if registration.lifestyle == LifeStyle.SINGLETON:
            if interface not in self._singletons:
                self._singletons[interface] = self._create(registration)
            return self._singletons[interface]

        # Scoped
        if registration.lifestyle == LifeStyle.SCOPED:
            if not self._scope_stack:
                raise RuntimeError("Scoped service requested outside the scope")
            scope = self._scope_stack[-1]
            if interface not in scope:
                scope[interface] = self._create(registration)
            return scope[interface]

        # PerRequest
        return self._create(registration)

    @contextmanager
    def create_scope(self):
        self._scope_stack.append({})
        try:
            yield self
        finally:
            self._scope_stack.pop()

    # noinspection PyMethodMayBeStatic
    def _create(self, registration: _Registration):
        provider = registration.provider
        if callable(provider) and not isinstance(provider, type):
            # Это фабрика
            return provider()
        return provider(**registration.params)
