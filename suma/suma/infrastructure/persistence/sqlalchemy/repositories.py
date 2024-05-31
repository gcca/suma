from typing import override

from sqlalchemy import exists, select
from sqlalchemy.exc import IntegrityError

from suma.domain.model.auth import AuthRepository, User, UsernameNotFoundError
from suma.domain.model.entry import Entry, EntryRepository

from . import db


class RepositorySA:

    __slots__ = ("db",)

    def __init__(self, db):
        self.db = db


class SAAuthRepository(AuthRepository, RepositorySA):

    @override
    async def Exists(self, username) -> bool:
        async with self.db() as session:
            query = select(exists().where(db.User.username == username))
            return bool((await session.execute(query)).scalar())

    @override
    async def Store(self, user: User):
        async with self.db() as session:
            session.add(
                db.User(username=user.username, password=user.password)
            )
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise

    @override
    async def Find(self, username) -> User:
        async with self.db() as session:
            result = await session.execute(
                select(db.User).filter_by(username=username)
            )
            db_user = result.scalars().first()
            if not db_user:
                raise UsernameNotFoundError(username)
            return User(username=db_user.username, password=db_user.password)


class SAEntryRepository(EntryRepository, RepositorySA):

    @override
    async def Store(self, entry: Entry) -> None:
        async with self.db() as session:
            session.add(
            )
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise
