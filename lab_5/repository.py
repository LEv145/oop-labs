import typing as t
from abc import ABC, abstractmethod

from sqlmodel import SQLModel, Session, select
from sqlalchemy import Engine

from user import User


T = t.TypeVar("T", bound=SQLModel)


class IDataRepository(t.Generic[T], ABC):
    @abstractmethod
    def get_all(self) -> t.Sequence[T]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> T | None:
        pass

    @abstractmethod
    def add(self, item: T) -> None:
        pass

    @abstractmethod
    def update(self, item: T) -> None:
        pass

    @abstractmethod
    def delete(self, item: T) -> None:
        pass


class DataRepository(IDataRepository[T], t.Generic[T]):
    def __init__(self, model: type[T], engine: Engine) -> None:
        self._model = model
        self._engine = engine

    def get_all(self) -> t.Sequence[T]:
        with Session(self._engine) as session:
            return list(session.exec(select(self._model)))

    def get_by_id(self, id: int) -> T | None:
        with Session(self._engine) as session:
            return session.get(self._model, id)

    def add(self, item: T) -> None:
        with Session(self._engine) as session:
            session.add(item)
            session.commit()
            session.refresh(item)

    def update(self, item: T) -> None:
        with Session(self._engine) as session:
            session.add(item)
            session.commit()
            session.refresh(item)

    def delete(self, item: T) -> None:
        with Session(self._engine) as session:
            session.delete(item)
            session.commit()


class IUserRepository(IDataRepository[User], ABC):
    @abstractmethod
    def get_by_login(self, login: str) -> User | None:
        pass


class UserRepository(DataRepository[User], IUserRepository):
    def __init__(self, engine: Engine) -> None:
        super().__init__(model=User, engine=engine)

    def get_by_login(self, login: str) -> User | None:
        with Session(self._engine) as session:
            sql = select(User).where(User.login == login)
            # noinspection PyTypeChecker
            return session.exec(sql).first()
