import uuid

import pytest
from sanic_testing.testing import SanicASGITestClient
from sqlalchemy import create_engine
from suma_web.main import app

from suma.infrastructure.persistence.sqlalchemy import db as _db
from suma.locator import Locator

DB_URL = "postgresql://postgres:postgres@localhost/suma"


@pytest.hookimpl
def pytest_sessionstart(session):
    engine = create_engine(DB_URL)
    _db.Base.metadata.drop_all(bind=engine)
    _db.Base.metadata.create_all(bind=engine)


@pytest.hookimpl
def pytest_sessionfinish(session, exitstatus):
    engine = create_engine(DB_URL)
    _db.Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    Locator.load()
    return SanicASGITestClient(app)


@pytest.fixture(scope="session")
def locator():
    return Locator


@pytest.fixture
def db():
    return lambda: Locator.db()


@pytest.fixture(scope="session")
def randstr():
    return lambda: str(uuid.uuid4())
