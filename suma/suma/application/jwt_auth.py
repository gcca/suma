import datetime
from typing import override

import jwt

from suma.application.services import (
    AuthenticationService,
    AuthorizationService,
    UserService,
)
from suma.domain.model.auth import AuthRepository
from suma.domain.shared import DomainError


class JWTServiceSupport:

    auth_repository: AuthRepository
    user_service: UserService

    __slots__ = ("auth_repository", "user_service")

    KEY = "Purvmx74X4A51-NBw980wPViJ_4ApFEd1Hrq8SNR4qrXK8fTHQDrFljeHhXyP6-C".encode()
    ALGORITHM = "HS256"

    def __init__(self, auth_repository, user_service):
        self.auth_repository = auth_repository
        self.user_service = user_service


class JWTAuthenticationService(AuthenticationService, JWTServiceSupport):

    @override
    async def Login(self, username, password):
        try:
            await self.user_service.Validate(username, password)
        except DomainError as error:
            raise LoginFailError() from error

        payload = {
            "username": username,
            "exp": datetime.datetime.now(datetime.UTC)
            + datetime.timedelta(days=1),
        }

        token = jwt.encode(
            payload=payload, key=self.KEY, algorithm=self.ALGORITHM
        )

        return token


class JWTAuthorizationService(AuthorizationService, JWTServiceSupport):

    @override
    async def ValdateLogin(self, token):
        try:
            payload = jwt.decode(token, self.KEY, [self.ALGORITHM])
        except jwt.ExpiredSignatureError as error:
            raise LoginRequiredError() from error

        return payload["username"]


class LoginFailError(DomainError):
    """Raised when login cannot find the user or password does not match."""

    def __str__(self):
        return "Usuario o contraseña no encontrados."


class LoginRequiredError(DomainError):

    def __str__(self):
        return "Sesión no válida."
