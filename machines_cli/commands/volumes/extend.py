import typer
from machines_cli.api import api
from machines_cli.logging import logger

app = typer.Typer(help="Extend machine volumes")


@app.command()
def extend(
    machine_name: str = typer.Argument(
        ..., help="Name of the machine to extend volume for"
    )
):
    """Extend a machine's storage volume to a specific size in GB"""
    try:
        # Verify machine exists
        machines = api.machines.get_machines(machine_name)
        if not machines:
            logger.error(f"Machine '{machine_name}' not found")
            raise typer.Exit(1)

        new_size = typer.prompt(
            f"Current volume size is for {machine_name} is {machines[0]['volume_size']} GB. Enter the new size for the volume in GB"
        )

        # Validate user want to expand, it is irreversible
        typer.confirm(
            f"Are you sure you want to extend the volume for machine '{machine_name}' to {new_size}GB? This action is irreversible."
        )

        # Extend the volume
        api.machines.extend_volume(machine_name, new_size)
        logger.success(f"Volume for machine '{machine_name}' extended to {new_size}GB")

    except Exception as e:
        logger.error(f"Failed to extend volume: {e}")
        raise typer.Exit(1)
