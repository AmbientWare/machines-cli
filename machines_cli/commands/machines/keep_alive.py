import typer

from machines_cli.api import api
from machines_cli.logging import logger

app = typer.Typer(help="List machines")


@app.command()
def keep_alive(name: str):
    """Keep a machine alive"""
    try:
        api.machines.keep_alive(name)

    except Exception as e:
        logger.error(f"Failed to keep machine alive: {e}")
        raise typer.Exit(1)
