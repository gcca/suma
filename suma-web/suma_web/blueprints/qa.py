from sanic import Blueprint, redirect
from sanic.views import HTTPMethodView
from sanic_ext import render

from .decorators import authorized

bp = Blueprint("qa", url_prefix="/qa")


@bp.get("/home")
@authorized
async def home(_):
    return await render("suma/qa/home.html")


class AddView(HTTPMethodView):

    template_name = "suma/qa/add.html"

    async def get(self, _):
        return await render(
            self.template_name, context={"title_focus": "autofocus"}
        )

    async def post(self, request):
        form = request.form
        title = form.get("title")
        content = form.get("content")
        tags = form.get("tags")

        if all((title, content, tags)):
            return await self._CreatePost(title, content, tags)
        else:
            return await self._ProcessMissingFields(title, content, tags)

    async def _CreatePost(self, title, content, tags):

        return redirect("/qa/home")

    async def _ProcessMissingFields(self, title, content, tags):
        context = {
            "title": title,
            "content": content,
            "tags": tags,
        }

        it = iter(
            (
                ("title_focus", title),
                ("content_focus", content),
                ("tags_focus", tags),
            )
        )

        for pair in it:
            if pair[1]:
                context[pair[0]] = ""
            else:
                context[pair[0]] = "autofocus"
                break

        while True:
            try:
                v = next(it)
                context[v[0]] = ""
            except StopIteration:
                break

        return await render(self.template_name, context=context)


bp.add_route(AddView.as_view(), "/add")
