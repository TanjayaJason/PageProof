from pathlib import Path
import typer
from .core import extract, answer
from .support import render_json
app = typer.Typer(help='Ask PDFs with page-linked evidence.', add_completion=False)

@app.command()
def ask(pdf: Path, question: str, ai: bool = False):
    """Read a PDF locally; --ai sends selected passages to your configured provider."""
    try:
        with pdf.open('rb') as handle:
            data = handle.read(20_000_001)
        typer.echo(render_json(answer(extract([(pdf.name, data)]), question, ai)))
    except Exception as exc:
        typer.echo(str(exc) if isinstance(exc, (ValueError, OSError)) else 'Unable to process PDF.', err=True)
        raise typer.Exit(1)
