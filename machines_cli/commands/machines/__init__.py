import typer

# Import command modules
from machines_cli.commands.machines.create import app as create_app
from machines_cli.commands.machines.scale import app as scale_app
from machines_cli.commands.machines.destroy import app as destroy_app
from machines_cli.commands.machines.get import app as get_app
from machines_cli.commands.machines.list import app as list_app
from machines_cli.commands.machines.connect import app as connect_app
from machines_cli.commands.machines.options import app as options_app

# Create the machines app
machines_app = typer.Typer(help="Machine management commands")

# Add command modules to the machines app
machines_app.add_typer(create_app)
machines_app.add_typer(scale_app)
machines_app.add_typer(destroy_app)
machines_app.add_typer(get_app)
machines_app.add_typer(list_app)
machines_app.add_typer(connect_app)
machines_app.add_typer(options_app)
