from abc import ABC, abstractmethod
from dataclasses import dataclass

from suma.domain.shared import DomainError


@dataclass
class User:
    username: str
    password: str


class UsernameNotFoundError(DomainError):
    """Raise when repository does not find username."""

    __slots__ = ("username",)

    def __init__(self, username):
        self.username = username

    def __str__(self):
        return f"Ya existe el usuario: {self.username}."


class AuthRepository(ABC):

    @abstractmethod
    async def Exists(self, username: str) -> bool: ...

    @abstractmethod
    async def Store(self, user: User) -> None: ...

    @abstractmethod
    async def Find(self, username: str) -> User: ...
