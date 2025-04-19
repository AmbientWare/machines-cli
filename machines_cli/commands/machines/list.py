import typer

from machines_cli.api import api
from machines_cli.logging import logger

app = typer.Typer(help="List machines")


@app.command()
def ls():
    """List all machines with optional filtering"""
    try:
        # Get machines from API
        machines = api.machines.list_machines()

        if not machines:
            logger.warning("No machines found")
            return

        # Display the table
        logger.table(machines)

    except Exception as e:
        logger.error(f"Failed to list machines: {e}")
        raise typer.Exit(1)
