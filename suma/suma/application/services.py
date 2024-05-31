from abc import ABC, abstractmethod

from suma.domain.model.entry import Entry


class UserService(ABC):

    @abstractmethod
    async def SignUp(self, username: str, password: str) -> None: ...

    @abstractmethod
    async def Validate(self, username: str, password: str) -> None: ...


class AuthenticationService(ABC):

    @abstractmethod
    async def Login(self, username: str, password: str) -> str: ...


class AuthorizationService(ABC):

    @abstractmethod
    async def ValdateLogin(self, token: str) -> None: ...


class QAService(ABC):

    @abstractmethod
    async def BookEntry(self, entry: Entry) -> None: ...
