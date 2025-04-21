import typer

# Import command modules
from machines_cli.commands.machines import machines_app
from machines_cli.commands.ssh import ssh_app
from machines_cli.commands.auth import auth_app
from machines_cli.commands.file_systems import fs_app

# Create the main app
app = typer.Typer(
    name="lazycloud",
    help="LazyCloud CLI",
    add_completion=False,
)

# Add command modules to the main app
app.add_typer(machines_app, name="machines")
app.add_typer(ssh_app, name="ssh")
app.add_typer(auth_app, name="auth")
app.add_typer(fs_app, name="fs")

if __name__ == "__main__":
    app()
