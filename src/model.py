import importlib
import pkgutil
from pathlib import Path

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


def import_models_from_package(package_name: str):
    """Import the 'models' submodule of a package if it exists."""
    try:
        importlib.import_module(f"{package_name}.models")
    except ModuleNotFoundError:
        pass

def discover_and_import_top_level_packages(app_package_name: str):
    """Discover all top-level packages under `app_package_name` and import their models."""
    app_package = importlib.import_module(app_package_name)
    app_path = Path(app_package.__file__).parent

    for _, name, is_pkg in pkgutil.iter_modules([str(app_path)]):
        if is_pkg:
            # Import the models submodule of each top-level package
            import_models_from_package(f"{app_package_name}.{name}")


discover_and_import_top_level_packages("src")
