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
        # Get file systems from API
        file_systems = api.file_systems.list_file_systems()
        fs_id = next(fs["id"] for fs in file_systems if fs["name"] == name)
        if not fs_id:
            logger.error(f"File system '{name}' not found")
            raise typer.Exit(1)

        api.file_systems.duplicate_file_system(id=fs_id, name=name)

        logger.success("File system duplicated successfully")

    except Exception as e:
        logger.error(f"Failed to duplicate file system: {e}")
        raise typer.Exit(1)
