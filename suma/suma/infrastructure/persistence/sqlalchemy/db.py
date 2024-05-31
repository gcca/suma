from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.schema import Column, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.sql.functions import now
from sqlalchemy.types import BigInteger, DateTime, Integer, String, Text

DB_URL = "postgresql+asyncpg://postgres:postgres@localhost/suma"
Base = declarative_base()


def MakeDb():
    engine = create_async_engine(DB_URL, echo=True)
    return async_sessionmaker(engine, expire_on_commit=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(
        String(length=100), unique=True, nullable=False, index=True
    )
    password = Column(String(length=250), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, server_default=now())


class Entry(Base):
    __tablename__ = "entries"
    __table_args__ = (
        PrimaryKeyConstraint("ax", "bx", name="entry_pk_constraint"),
    )

    ax = Column(BigInteger, nullable=False, index=True)
    bx = Column(BigInteger, nullable=False, index=True)
    title = Column(String(length=140), nullable=False)
    content = Column(Text, nullable=False)


class EntryTag(Base):
    __tablename__ = "entrytags"

    name = Column(String(length=100), primary_key=True)
    ax = Column(BigInteger, ForeignKey("entries.ax"), nullable=False)
    bx = Column(BigInteger, ForeignKey("entries.bx"), nullable=False)
