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
    try:
        # Use Typer's built-in rich text formatting
        confirm = typer.confirm(
            typer.style(
                f"Are you sure you want to delete file system {name}?",
                fg=typer.colors.RED,
                bold=True,
            )
        )
        if not confirm:
            return

        fs = api.file_systems.get_file_system(name)
        if not fs:
            logger.error(f"File system {name} not found")
            raise typer.Exit(1)

        fs_id = fs.get("id")
        if not fs_id:
            logger.error(f"File system {name} has no ID")
            raise typer.Exit(1)

        result = api.file_systems.delete_file_system(fs_id)
        if result:
            logger.success(f"Successfully destroyed file system {name}")
        else:
            logger.error(f"Failed to destroy file system {name}")

    except Exception as e:
        logger.error(f"Error deleting file system: {e}")
