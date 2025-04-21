import typer
from machines_cli.api import api
from machines_cli.logging import logger
import click

app = typer.Typer(help="Extend machine volumes")


@app.command()
def create(name: str = typer.Argument(..., help="Name of the file system to create")):
    """Create a new file system"""
    try:
        # Verify file system does not exist
        file_systems = api.file_systems.get_file_system(name)
        if file_systems:
            logger.error(f"File system '{name}' already exists")
            raise typer.Exit(1)

        # NOTE: regions is dependent on the machine options
        machine_options = api.machines.get_machine_options()
        if not machine_options:
            logger.error(
                "No machine options found. Please create a machine first with `lazycloud machines create`"
            )
            return

        # prompt to get the region
        regions = machine_options.regions
        region = logger.option("Available regions:", regions, default="lax")

        # prompt to get the size with validation
        size = typer.prompt(
            "Enter the size of the file system in GB. Minimum size is 10GB.",
            default=10,
            type=click.IntRange(min=10),
        )

        # Create file system
        api.file_systems.create_file_system(name, size, region)
        logger.success(f"File system '{name}' created successfully")

    except Exception as e:
        logger.error(f"Failed to create file system: {e}")
        raise typer.Exit(1)
