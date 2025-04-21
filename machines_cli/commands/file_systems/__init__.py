import typer

# Import command modules
from machines_cli.commands.file_systems.extend import app as extend_app
from machines_cli.commands.file_systems.create import app as create_app
from machines_cli.commands.file_systems.destroy import app as destroy_app
from machines_cli.commands.file_systems.list import app as list_app

# Create the volumes app
fs_app = typer.Typer(help="File system management commands")

# Add command modules to the volumes app
fs_app.add_typer(extend_app)
fs_app.add_typer(create_app)
fs_app.add_typer(destroy_app)
fs_app.add_typer(list_app)
