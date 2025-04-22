import typer
import subprocess

from machines_cli.api import api
from machines_cli.logging import logger
from machines_cli.ssh_config import ssh_config_manager

app = typer.Typer(help="Connect to machines")


@app.command()
def connect(
    name: str = typer.Argument(..., help="Name of the machine to connect to"),
    command: str = typer.Option(
        None, "--command", "-c", help="Command to execute on the remote machine"
    ),
):
    """Connect to a machine via SSH"""
    try:
        # Get machine details from API
        machines = api.machines.get_machines(name)
        if not machines:
            logger.error(f"Machine '{name}' not found")
            raise typer.Exit(1)

        machine = machines[0]  # Get the first (and should be only) machine

        # Get machine connection details
        alias, port = api.machines.get_machine_alias(name)
        if not alias or not port:
            logger.error(f"Failed to get connection details for machine '{name}'")
            raise typer.Exit(1)

        # Ensure SSH config is up to date
        ssh_config_manager.add_machine(
            machine_name=name,
            alias=alias,
            port=port,
        )

        # Build SSH command
        ssh_cmd = ["ssh", name]
        if command:
            ssh_cmd.extend(["-t", command])

        # Execute SSH command
        logger.status(f"Connecting to {name}...")
        subprocess.run(ssh_cmd)

    except Exception as e:
        logger.error(f"Failed to connect to {name}: {e}")
        raise typer.Exit(1)
