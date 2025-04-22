import typer
from machines_cli.config import config
from machines_cli.logging import logger

app = typer.Typer(help="Remove an API key")


@app.command()
def rm(
    name: str = typer.Argument(..., help="Name of the API key to remove"),
):
    """Remove an API key"""
    try:
        # Check if key exists
        if name not in config.list_api_keys():
            logger.error(f"API key '{name}' not found")
            raise typer.Exit(1)

        # Confirm removal
        if not typer.confirm(f"Are you sure you want to remove API key '{name}'?"):
            return

        # Remove the key
        config.remove_api_key(name)
        logger.success(f"Removed API key '{name}'")

    except Exception as e:
        logger.error(f"Failed to remove API key: {e}")
        raise typer.Exit(1)
