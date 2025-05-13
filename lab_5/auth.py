from abc import ABC, abstractmethod

from user import User
from repository import IUserRepository


class IAuthService(ABC):
    @abstractmethod
    def sign_in(self, user: User) -> None:
        pass

    @abstractmethod
    def sign_out(self) -> None:
        pass

    @property
    @abstractmethod
    def is_authorized(self) -> bool:
        pass

    @property
    @abstractmethod
    def current_user(self) -> User | None:
        pass


class AuthService(IAuthService):
    def __init__(self, user_repository: IUserRepository) -> None:
        self._repository = user_repository
        self._current_user: User | None = None

        self._restore_session()

    def sign_in(self, user: User) -> None:
        for other in self._repository.get_all():
            if other.is_logged_in and user.id != other.id:
                other.is_logged_in = False
                self._repository.update(other)

        user.is_logged_in = True
        self._repository.update(user)
        self._current_user = user
        print(f"✅ Пользователь {user.login} вошёл в систему")

    def sign_out(self) -> None:
        if not self._current_user:
            return

        self._current_user.is_logged_in = False
        self._repository.update(self._current_user)
        print(f"🚪 Пользователь {self._current_user.login} вышел")
        self._current_user = None

    def _restore_session(self) -> None:
        logged = [user for user in self._repository.get_all() if user.is_logged_in]
        if logged:
            self._current_user = logged[0]
            print(f"🔄 Авто‑авторизован как {self._current_user.login}")

    @property
    def is_authorized(self) -> bool:
        return self._current_user is not None

    @property
    def current_user(self) -> User | None:
        return self._current_user
