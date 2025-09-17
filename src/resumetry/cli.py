from pathlib import Path
from rich.console import Console
from typing_extensions import Annotated, Optional
from importlib.metadata import version as pkg_version, PackageNotFoundError
from importlib.resources import files
import typer
from .utils import Utils
from .validators import Validators

app = typer.Typer(
    name="resumetry",
    rich_markup_mode="rich",
    context_settings={"help_option_names": ["--help", "-h"]},
    add_completion=False,
)

console = Console()

def _version_callback(value: bool):
    if not value:
        return value
    try:
        v = pkg_version("resumetry")
    except PackageNotFoundError:
        try:
            from . import __version__ as v
        except Exception:
            v = "0.0.0+dev"
    typer.echo(v)
    raise typer.Exit()


@app.callback(invoke_without_command=True)
def build(
    config: Annotated[str, typer.Option("--config", "-c", help = "path to the config yaml file ")],
    template: Annotated[Optional[str], typer.Option("--template", "-t", help = "predefined LaTex template", callback=Validators.choices)] = 'sample',
    template_path: Annotated[Optional[str], typer.Option("--template-path", help = "path to LaTex template")] = None,
    output: Annotated[str, typer.Option("--output", "-o", help = "path to the output file")]  = "./output.pdf",
    engine: Annotated[str, typer.Option("--engine", "-e", help="pdflatex | xelatex | lualatex")] = "pdflatex",
    version: Annotated[
            bool,
            typer.Option(
                "--version", "-V",
                help="Show resumetry version and exit",
                is_flag=True,
                is_eager=True,
                callback=_version_callback,
            ),
        ] = False,
):
    cfg_path = Path(config)
    out_path = Path(output)

    tpl_path = Path(template_path) if template_path else files("resumetry").joinpath(f"templates/{template}/{template}.tex")
    console.print(f"[green]✓ Read template[/green] [dim]{tpl_path}")

    data = Utils.read_yaml(cfg_path)
    console.print(f"[green]✓ Read config[/green] [dim]{cfg_path}")

    tex = Utils.render_tex(tpl_path, data)
    Utils.save_tex(tex)
    console.print(f"[green]✓ Populated template[/green] [dim]{tpl_path}")

    Utils.run_pdflatex(tex, out_path, engine=engine)
    console.print(f"[green]✓ Generated[/green] [dim]{out_path}")


if __name__ == "__main__":
    app()
