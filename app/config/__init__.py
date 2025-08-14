import os

env = os.getenv("APP_SETTINGS", "dev").lower()

if env == "dev":
    from .dev import _dev_settings
elif env == "prod":
    from .prod import _prod_settings
else:
    raise EnvironmentError("APP_SETTINGS environment variable is not set")

settings = _dev_settings if env else _prod_settings

__all__ = ["settings"]