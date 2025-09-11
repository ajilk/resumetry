from pathlib import Path
from rich.console import Console
from typing_extensions import Annotated, Optional
import typer
from utils import Utils

TEMPLATES_LIST = ["sample"]

app = typer.Typer(
    name="resumetry",
    rich_markup_mode="rich",
    context_settings={"help_option_names": ["--help", "-h"]},
    add_completion=False,
)

console = Console()

def validate_path(value: str):
    if value and not Path(value).exists():
        raise typer.BadParameter(value)
    return value

def validate_choices(value: str):
    if value and value not in TEMPLATES_LIST:
        raise typer.BadParameter(f"Supported values {TEMPLATES_LIST}")
    return value

@app.command()
def main(
    config: Annotated[str, typer.Option("--config", "-c", help = "path to the config yaml file ", callback=validate_path)] = "./config.yaml",
    template: Annotated[Optional[str], typer.Option("--template", "-t", help = "predefined LaTex template", callback=validate_choices)] = None,
    template_path: Annotated[Optional[str], typer.Option("--template-path", help = "path to the template LaTeX file", callback=validate_path)] = None,
    output: Annotated[str, typer.Option("--output", "-o", help = "path to the output file")]  = "./output.pdf",
    engine: Annotated[str, typer.Option("--engine", "-e", help="pdflatex | xelatex | lualatex")] = "pdflatex",
):
    if bool(template_path) == bool(template):
        raise typer.BadParameter(
            "You must provide either --template-path OR --template, but not both."
        )

    cfg_path, out_path = Path(config), Path(output)
    tpl_path = Path(template_path) if template_path else Path(f"./templates/{template}/{template}.tex")

    data = Utils.read_yaml(cfg_path)
    console.print(f"[green]✓ Read config[/green] [dim]{cfg_path}")

    tex = Utils.render_tex(tpl_path, data)
    Utils.save_tex(tex)
    console.print(f"[green]✓ Populated template[/green] [dim]{tpl_path}")

    Utils.run_pdflatex(tex, out_path, engine=engine)
    console.print(f"[green]✓ Generated[/green] [dim]{out_path}")


if __name__ == "__main__":
    app()
