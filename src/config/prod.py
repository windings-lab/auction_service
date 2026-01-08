from .base import Settings


class ProdSettings(Settings):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)