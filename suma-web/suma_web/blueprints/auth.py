from sanic import Blueprint
from sanic.response import redirect
from sanic.views import HTTPMethodView
from sanic_ext import render

from suma.domain.shared import DomainError
from suma.locator import Locator

bp = Blueprint("auth", url_prefix="/auth")


class LoginView(HTTPMethodView):

    template_name = "suma/auth/login.html"

    async def get(self, request):
        if "unauthorized" in request.args:
            return await render(
                self.template_name,
                context={"error_message": "Ingreso no autorizado."},
            )
        return await render(self.template_name)

    async def post(self, request, locator: Locator):
        username = request.form.get("username")
        password = request.form.get("password")

        not_provided_fields = []
        if not username:
            not_provided_fields.append("username")
        if not password:
            not_provided_fields.append("password")
        if not_provided_fields:
            error_message = " and ".join(not_provided_fields) + " not provided"
            return await render(
                self.template_name, context=dict(error_message=error_message)
            )

        match request.form.get("entry"):
            case "login":
                return await self._authenticate(locator, username, password)
            case "signup":
                return await self._signup(locator, username, password)

        return await render(
            self.template_name, context=dict(error_message="No entry provided")
        )

    async def _signup(self, locator, username, password):
        try:
            await locator.user_service.SignUp(username, password)
        except DomainError as error:
            return await render(
                self.template_name,
                context=dict(error_message=str(error)),
            )

        return redirect("/auth/login")

    async def _authenticate(self, locator, username, password):
        try:
            token = await locator.authentication_service.Login(
                username, password
            )
        except DomainError as error:
            return await render(
                self.template_name,
                context=dict(error_message=str(error)),
            )

        response = redirect("/qa/home")
        response.add_cookie("bearer", token, secure=False, max_age=65535)

        return response


bp.add_route(LoginView.as_view(), "/login")
