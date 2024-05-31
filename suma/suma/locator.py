from typing import ClassVar

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from suma.application.h_user import HUserService
from suma.application.jwt_auth import (
    JWTAuthenticationService,
    JWTAuthorizationService,
)
from suma.application.services import (
    AuthenticationService,
    AuthorizationService,
    UserService,
)
from suma.domain.model.auth import AuthRepository
from suma.infrastructure.persistence.sqlalchemy.db import MakeDb
from suma.infrastructure.persistence.sqlalchemy.repositories import (
    SAAuthRepository,
)


class Locator:

    db: ClassVar[async_sessionmaker[AsyncSession]]
    auth_repository: ClassVar[AuthRepository]
    user_service: ClassVar[UserService]
    authentication_service: ClassVar[AuthenticationService]
    authorization_service: ClassVar[AuthorizationService]

    @classmethod
    def load(cls):
        cls.db = MakeDb()
        cls.auth_repository = SAAuthRepository(cls.db)
        cls.user_service = HUserService(cls.auth_repository)
        cls.authentication_service = JWTAuthenticationService(
            cls.auth_repository, cls.user_service
        )
        cls.authorization_service = JWTAuthorizationService(
            cls.auth_repository, cls.user_service
        )

    @classmethod
    def loaded(cls):
        return hasattr(cls, "db")
