import typer

from machines_cli.api import api
from machines_cli.logging import logger
from machines_cli.ssh_config import ssh_config_manager

app = typer.Typer(help="Delete a machine")


@app.command()
def destroy(
    name: str = typer.Argument(..., help="Name of the file system to delete"),
):
    """Delete a file system"""
    logger.confirm(f"Are you sure you want to delete file system {name}?")

    try:
        result = api.file_systems.delete_file_system(name)
        if result:
            logger.success(f"Successfully destroyed file system {name}")
        else:
            logger.error(f"Failed to destroy file system {name}")

    except Exception as e:
        logger.error(f"Error deleting file system: {e}")
