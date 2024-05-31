from functools import wraps
from typing import Awaitable, Callable, Concatenate, Optional

from sanic import HTTPResponse, Request, redirect

from suma.domain.shared import DomainError
from suma.locator import Locator

UNAUTHORIZED_URL = "/auth/login?unauthorized="


def authorized[
    **T
](f: Callable[Concatenate[Request, T], Awaitable[HTTPResponse]]) -> Callable[
    Concatenate[Request, T], Awaitable[HTTPResponse]
]:
    @wraps(f)
    async def wrap(
        request: Request, *args: T.args, **kwargs: T.kwargs
    ) -> HTTPResponse:
        token: Optional[str] = request.cookies.get("bearer")
        if token is None:
            return redirect(UNAUTHORIZED_URL + "no-token")

        try:
            request.ctx.username = (
                await Locator.authorization_service.ValdateLogin(token)
            )
            return await f(request, *args, **kwargs)
        except DomainError as error:
            return redirect(UNAUTHORIZED_URL + str(error))

    return wrap
