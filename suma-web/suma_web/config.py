from pathlib import Path

from sanic.config import Config as SanicConfig


class Config(SanicConfig):
    # paths
    PROJECT_DIR = Path(__file__).resolve().parent
    # static
    PUBLIC_URL = "/public"
    PUBLIC_DIR = f"{PROJECT_DIR}/public"


config = Config()
