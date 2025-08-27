import os
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

env = config.get("app", "settings", fallback=os.getenv("APP_SETTINGS", "dev").lower())

settings = None

if env == "dev":
    from .dev import _dev_settings
    settings = _dev_settings
elif env == "prod":
    from .prod import _prod_settings
    settings = _prod_settings
else:
    raise EnvironmentError("APP_SETTINGS environment variable is not set")

__all__ = ["settings"]