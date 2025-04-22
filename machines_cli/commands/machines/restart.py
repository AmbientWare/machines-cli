import typer

from machines_cli.api import api
from machines_cli.logging import logger

app = typer.Typer(help="List machines")


@app.command()
def restart(name: str):
    """Restart a machine"""
    try:
        api.machines.restart(name)

    except Exception as e:
        logger.error(f"Failed to restart machine: {e}")
        raise typer.Exit(1)
