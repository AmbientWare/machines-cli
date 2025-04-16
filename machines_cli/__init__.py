# Import modules to register their commands
from machines_cli.commands import app
import machines_cli.commands.machines
import machines_cli.commands.ssh
import machines_cli.commands.volumes
import machines_cli.commands.keys


__all__ = ["app"]
