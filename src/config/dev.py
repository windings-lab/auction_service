from .base import Settings

class DevSettings(Settings):
    def __init__(self, config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)