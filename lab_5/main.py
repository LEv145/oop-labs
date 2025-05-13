from datetime import date

from sqlmodel import create_engine, SQLModel

from user import User
from repository import UserRepository
from auth import AuthService


def main() -> None:
    engine = create_engine(f"sqlite:///meow.db", echo=False)
    SQLModel.metadata.create_all(engine)

    repo = UserRepository(engine=engine)
    auth = AuthService(repo)

    print("=== Текущее содержимое БД ===")
    for user in sorted(repo.get_all()):
        print(user)

    admin = repo.get_by_login("admin")
    if not admin:
        print("=== Добавление admin === ")
        admin = User(name="Администратор", login="admin", password="admin123", email="root@example.com")
        repo.add(admin)
        print("Добавлен:", admin)

    # авторизуем admin
    print("=== Авторизация admin ===")
    auth.sign_in(admin)

    # изменим email
    print("=== Редактирование admin (email) ===")
    admin.email = f"admin@{date.today().year}.corp"
    repo.update(admin)
    print("После update:", admin)

    print("=== Смена пользователя -> guest ===")
    guest = repo.get_by_login("guest")
    if guest is None:
        guest = User(name="Гость", login="guest", password="guest")
        repo.add(guest)
    auth.sign_in(guest)

    print("=== Итоговое содержимое БД ===")
    for user in sorted(repo.get_all()):
        status = " <− текущий" if user.is_logged_in else ""
        print(user, status)

    print("\n🔁 Перезапустите программу — система автоматически авторизует `guest`")


if __name__ == "__main__":
    main()
