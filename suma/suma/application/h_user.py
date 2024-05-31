import hashlib
import hmac
from typing import override

from suma.domain.model.auth import AuthRepository, User, UsernameNotFoundError
from suma.domain.shared import DomainError
from suma.application.services import UserService


class HUserService(UserService):

    auth_repository: AuthRepository

    __slots__ = "auth_repository",

    def __init__(self, auth_repository):
        self.auth_repository = auth_repository

    KEY = "VPoEiE2gyJNteC8GYnMCoKX6CJR1kEUEN4t5wVW_aLKprG4Nqd3W6NEXxWCMQ1cZ".encode()

    @override
    async def SignUp(self, username, password):
        if await self.auth_repository.Exists(username):
            raise UsernameNotFoundError(username)

        hashed_password = self._HashPassword(username, password)
        user = User(username, hashed_password)
        await self.auth_repository.Store(user)

    @override
    async def Validate(self, username, password):
        try:
            user = await self.auth_repository.Find(username)
        except UsernameNotFoundError as error:
            raise InvalidUsernamePassword() from error

        hashed_password = self._HashPassword(username, password)
        if not hmac.compare_digest(hashed_password, user.password):
            raise InvalidUsernamePassword()


    @staticmethod
    def _HashPassword(username, password):
        return hmac.new(
            HUserService.KEY,
            f"{username}:{password}".encode(),
            hashlib.sha256,
        ).hexdigest()


class InvalidUsernamePassword(DomainError):

    def __str__(self):
        return "Usuario o contraseña inválidos."
