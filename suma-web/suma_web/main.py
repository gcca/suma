from sanic import Sanic
from sanic.response import redirect, text
from suma_web.config import config

from .blueprints.auth import bp as auth_bp
from .blueprints.qa import bp as qa_bp

app = Sanic("suma-web", config=config)

app.static(config.PUBLIC_URL, config.PUBLIC_DIR)

app.blueprint(auth_bp)
app.blueprint(qa_bp)


@app.before_server_start
async def setup(app, _):
    from jinja2 import PackageLoader, select_autoescape

    from suma.locator import Locator

    if not Locator.loaded():
        Locator.load()
    app.ext.add_dependency(Locator, lambda: Locator)

    app.ext.environment.loader = PackageLoader("suma_web.blueprints")
    app.ext.environment.autoescape = select_autoescape()
    app.ext.environment.globals.update(
        {
            "config": config,
        }
    )


@app.get("/check")
async def check(_):
    return text("Suma 😎")


@app.get("/")
async def index(_):
    return redirect("/auth/login")
