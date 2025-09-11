from pathlib import Path
import typer

TEMPLATES_LIST = ["sample"]

class Validators:
    @staticmethod
    def path(value: str):
        if value and not Path(value).exists():
            raise typer.BadParameter(value)
        return value

    @staticmethod
    def choices(value: str):
        if value and value not in TEMPLATES_LIST:
            raise typer.BadParameter(f"Supported values {TEMPLATES_LIST}")
        return value
