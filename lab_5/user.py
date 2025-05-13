import typing as t

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int  | None = Field(default=None, primary_key=True)
    name: str
    login: str = Field(index=True, unique=True)
    password: str = Field(repr=False)
    email: str | None = None
    address: str | None = None
    is_logged_in: bool = Field(default=False, repr=False)

    def __lt__(self, other: t.Self) -> bool:
        return self.name.lower() < other.name.lower()
