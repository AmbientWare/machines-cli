import typer
from rich.console import Console
import click

from machines_cli.api import api
from machines_cli.logging import logger
from machines_cli.ssh_config import ssh_config_manager

app = typer.Typer(help="Create a new machine")
console = Console()


@app.command()
def create(
    machine_name: str = typer.Argument(None, help="Name of the machine to create"),
):
    """Create a new machine"""
    try:
        # make sure the machine name is not already taken
        if api.machines.get_machines(machine_name):
            logger.error(
                f"Machine '{machine_name}' already exists. Please choose a different name."
            )
            return

        ssh_keys = api.ssh_keys.get_ssh_keys()
        if not ssh_keys:
            logger.error(
                "No SSH keys found. Please create an SSH key first with `lazycloud ssh add`"
            )
            return

        machine_options = api.machines.get_machine_options()
        if not machine_options:
            logger.error(
                "No machine options found. Please create a machine first with `lazycloud machines create`"
            )
            return

        # prompt to get the region
        regions = machine_options.regions
        region = logger.option("Available regions:", regions, default="lax")

        # prompt to get the cpu
        cpu_options = machine_options.options.keys()
        cpu = logger.option("Available CPU options:", [str(cpu) for cpu in cpu_options])

        # prompt to get the memory
        memory_options = machine_options.options[cpu]
        memory = logger.option(
            "Available RAM options (GB):", [str(memory) for memory in memory_options]
        )

        # prompt to get the gpu kind
        gpu_kind = typer.prompt(
            "Select the GPU kind",
            default="None",
        )

        # Ask which ssh key the user wants to use
        try:
            key_names = [key["name"] for key in ssh_keys]
            ssh_key_name = logger.option(
                "Available SSH keys:",
                key_names,
            )

        except FileNotFoundError as e:
            logger.error(str(e))
            return

        except Exception as e:
            logger.error(f"Error reading public key file: {e}")
            return

        # have user input the volume size, default to 10
        file_systems = api.file_systems.list_file_systems()
        if file_systems:
            fs_names = [fs["name"] for fs in file_systems] + ["None"]
            file_system_name = logger.option(
                "Select a file system or leave blank to create a new one",
                fs_names,
                default="None",
            )
        else:
            logger.warning(
                "No file systems found. you will need to create a file system first."
            )
            file_system_name = "None"

        if file_system_name == "None":
            file_system_name = typer.prompt("Enter the name of the file system")
            file_system_size = typer.prompt(
                "Enter the size of the file system in GB. Minimum size is 10GB.",
                default=10,
                type=click.IntRange(min=10),
            )
            # create a new file system if wants to
            file_system = api.file_systems.create_file_system(
                file_system_name, file_system_size, region
            )

        else:
            file_system = api.file_systems.get_file_system(file_system_name)

        fs_id = file_system.get("id")
        if not fs_id:
            logger.error(f"File system '{file_system_name}' not found")
            return

        # Create machine using API
        try:
            result = api.machines.create_machine(
                name=machine_name,
                public_key=ssh_key_name,
                region=region,
                cpu=int(cpu),
                memory=int(memory),
                file_system_id=fs_id,
                gpu_kind=gpu_kind if gpu_kind != "None" else None,
            )

            if result:
                created_machine = api.machines.get_machines(machine_name)
                if created_machine:
                    logger.table(created_machine)

        except Exception as e:
            logger.error(f"Error creating machine: {e}")
            return

        # add to ssh config
        alias, port = api.machines.get_machine_alias(machine_name)
        if alias is None or port is None:
            logger.error(
                "Error getting machine alias. Please try again by running `machines connect add <machine-name>`."
            )
            return

        ssh_config_manager.add_machine(machine_name, alias, port)
        logger.success(f"Added machine {machine_name} to SSH config")
        logger.success(
            f"Machine created successfully. You can now connect to it using `lazycloud machines connect {machine_name}`"
        )

    except Exception as e:
        logger.error(f"Error creating machine: {e}")
