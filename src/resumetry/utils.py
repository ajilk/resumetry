import subprocess, tempfile, shutil
from pathlib import Path
import yaml

from jinja2 import Environment, DictLoader, StrictUndefined
from importlib.resources.abc import Traversable

class Utils:
    @staticmethod
    def read_yaml(path: Traversable) -> dict:
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    @staticmethod
    def render_tex(path: Traversable, context: dict) -> str:
        env = Environment(
            loader=DictLoader({"_": path.read_text()}),
            undefined=StrictUndefined,
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
            comment_start_string='<%',
            comment_end_string='%>',
            variable_start_string="\\VAR{",
            variable_end_string="}",
        )
        tmpl = env.get_template("_")
        return tmpl.render(**context)

    @staticmethod
    def run_pdflatex(tex_source: str, out_pdf: Path, engine: str = "pdflatex") -> None:
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            tex_file = tmp / "doc.tex"
            tex_file.write_text(tex_source, encoding="utf-8")

            cmd = [engine, "-interaction=nonstopmode", "-halt-on-error", tex_file.name]
            for _ in range(2):
                proc = subprocess.run(cmd, cwd=tmp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                if proc.returncode != 0:
                    raise SystemExit(proc.stdout)

            pdf_path = tmp / "doc.pdf"
            out_pdf.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(pdf_path, out_pdf)

    @staticmethod
    def save_tex(content: str, out_path: str = "./.generated.tex") -> Path:
        out_file = Path(out_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(content, encoding="utf-8")
        return out_file
