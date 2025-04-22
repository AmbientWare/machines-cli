import typer

from machines_cli.api import api
from machines_cli.logging import logger

app = typer.Typer(help="Duplicate a file system")


@app.command()
def duplicate(
    name: str = typer.Argument(..., help="Name of the file system to duplicate")
):
    """Duplicate a file system"""
    try:
        api.file_systems.duplicate_file_system(name, name)

        logger.success("File system duplicated successfully")

    except Exception as e:
        logger.error(f"Failed to duplicate file system: {e}")
        raise typer.Exit(1)
