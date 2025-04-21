# Import modules to register their commands
from machines_cli.commands import app
import machines_cli.commands.machines
import machines_cli.commands.ssh
import machines_cli.commands.file_systems
import machines_cli.commands.auth


__all__ = ["app"]
