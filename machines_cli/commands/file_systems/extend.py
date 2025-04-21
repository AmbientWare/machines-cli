import typer
from machines_cli.api import api
from machines_cli.logging import logger

app = typer.Typer(help="Extend machine volumes")


@app.command()
def extend(
    name: str = typer.Argument(..., help="Name of the file system to extend volume for")
):
    """Extend a file system's storage volume to a specific size in GB"""
    try:
        # Verify file system exists
        file_system = api.file_systems.get_file_system(name)

        new_size = typer.prompt(
            f"Current volume size is for {name} is {file_system['size']} GB. Enter the new size for the volume in GB"
        )

        # Validate user want to expand, it is irreversible
        typer.confirm(
            f"Are you sure you want to extend the volume for file system '{name}' to {new_size}GB? This action is irreversible."
        )

        # Extend the volume
        api.file_systems.extend_volume(file_system["id"], new_size)
        logger.success(f"Volume for file system '{name}' extended to {new_size}GB")

    except Exception as e:
        logger.error(f"Failed to extend volume: {e}")
        raise typer.Exit(1)
