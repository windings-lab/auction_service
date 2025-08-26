from .base import Settings

class DevSettings(Settings):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


_dev_settings = DevSettings(_env_file='.env', _env_file_encoding='utf-8')