import typer
from importlib.resources import files

TEMPLATES_LIST = ["sample", "main"]

class Validators:
    @staticmethod
    def path(value: str):
        # check for valid path and not just under resumetry
        if value and not files("resumetry").joinpath(value).is_file():
            raise typer.BadParameter(value)
        return value

    @staticmethod
    def choices(value: str):
        if value and value not in TEMPLATES_LIST:
            raise typer.BadParameter(f"Supported values {TEMPLATES_LIST}")
        return value
