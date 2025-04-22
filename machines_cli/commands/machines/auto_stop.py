import typer

from machines_cli.api import api
from machines_cli.logging import logger

app = typer.Typer(help="List machines")


@app.command()
def auto_stop(name: str):
    """Auto stop a machine"""
    try:
        api.machines.auto_stop(name)

    except Exception as e:
        logger.error(f"Failed to auto stop machine: {e}")
        raise typer.Exit(1)
