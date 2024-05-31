from typing import Type

import pytest
from sqlalchemy import text

from suma.locator import Locator

pytestmark = pytest.mark.asyncio


@pytest.fixture
def username(randstr):
    return randstr()


class TestSignUp:

    async def test_signup_new_user(self, client, db, username):
        _, response = await client.post(
            "/auth/login",
            data={"username": username, "password": "foo", "entry": "signup"},
        )

        assert response.status == 302
        assert response.headers["location"] == "/auth/login"

        async with db() as session:
            result = await session.execute(
                text(f"SELECT 1 FROM users WHERE username = '{username}'")
            )

        assert result.rowcount == 1

    async def test_signup_already_app_user(self, client, db, username):
        async with db() as session:
            await session.execute(
                text(
                    f"INSERT INTO users(username, password) VALUES ('{username}', 'foo')"
                )
            )
            await session.commit()

        _, response = await client.post(
            "/auth/login",
            data={"username": username, "password": "bar", "entry": "signup"},
        )

        assert response.status == 200
        assert f"Ya existe el usuario: {username}.".encode() in response.body


class TestLogIn:

    async def test_login_user(self, client, username, locator: Type[Locator]):
        await locator.user_service.SignUp(username, "foo")

        _, response = await client.post(
            "/auth/login",
            data={"username": username, "password": "foo", "entry": "login"},
        )

        assert response.status == 302
        assert response.headers["location"] == "/qa/home"
        assert "bearer" in response.cookies

    async def test_fail_login(self, client, username):
        _, response = await client.post(
            "/auth/login",
            data={"username": username, "password": "foo", "entry": "login"},
        )

        assert response.status == 200
        assert "Usuario o contraseña no encontrados.".encode() in response.body


class TestSession:

    async def test_redirect(self, client):
        _, response = await client.get("/qa/home")

        assert response.status == 302
        assert (
            response.headers["location"] == "/auth/login?unauthorized=no-token"
        )

    async def test_login_page_message(self, client):
        _, response = await client.get("/auth/login?unauthorized=t")

        assert "Ingreso no autorizado.".encode() in response.body

    async def test_authorized(self, client, username, locator: Type[Locator]):
        await locator.user_service.SignUp(username, "foo")
        await client.post(
            "/auth/login",
            data={"username": username, "password": "foo", "entry": "login"},
        )

        request, response = await client.get("/qa/home")

        assert response.status == 200
        assert "bearer" in request.cookies
