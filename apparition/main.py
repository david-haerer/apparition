from pathlib import Path
import os

import typer
import rich

from apparition.exceptions import ConfigError
from apparition import utils


def check():
    """Wrap utils.check_os() and use utils.error() on OSError."""
    try:
        utils.check_os()
    except OSError as message:
        utils.error(message)


def save(data: dict[str, Path]):
    """Wrap utils.save_config_data() and use utils.error() on ConfigError."""
    try:
        utils.save_config_data(data)
    except ConfigError as message:
        utils.error(message)


def load() -> dict[str, Path]:
    """Wrap utils.load_config_data() and use utils.error() on ConfigError."""
    try:
        data = utils.load_config_data()
    except ConfigError as message:
        utils.error(message)
    return data


app = typer.Typer(add_completion=False)
console = rich.console.Console()
shellrc = utils.get_shell_config_file()
check()


@app.command(
    help=(
        f"Add the output of this command to your '{shellrc}'.\n\n"
        f"You can do this by running 'apparition install >> {shellrc}'.\n\n"
        f"Then run 'source {shellrc}'."
        f"This creates a shell function called apparate that can change the working directory in a safe manner."
    )
)
def install():
    """Help text is given in the @app.command() decorator to use the correct shellrc."""
    apparate = utils.load_apparate_shell_function()
    for line in apparate:
        rich.print(line)


@app.command()
def set(destination: str, path: Path):
    """Set a new destination.

    This command can also be used to update an existing destination.
    """
    data = load()
    data[destination] = path
    save(data)


@app.command()
def remove(destination: str):
    """Remove a destination."""
    data = load()
    del data[destination]
    save(data)


@app.command()
def rename(old_name: str, new_name: str):
    """Rename a destination."""
    data = load()
    data[new_destination] = data[old_destination]
    del data[old_destination]
    save(data)


@app.command()
def show(list: bool = typer.Option(False, help=f"Give a simple output.")):
    """Show all destinations."""
    data = load()
    if list:
        for destination in sorted(data.keys()):
            path = data[destination]
            rich.print(f"[bold]{destination}:[/bold] {str(path.resolve())}")
    else:
        table = rich.table.Table("Destination", "Path")
        for destination in sorted(data.keys()):
            path = data[destination]
            table.add_row(destination, str(path.resolve()))
        console.print(table)


@app.command()
def purge(
    yes: bool = typer.Option(
        False,
        help=f"Don't ask for confirmation.",
        prompt="Are you sure you want to delete all destinations?",
    )
):
    """Remove all destinations."""
    if not yes:
        raise typer.Exit(1)
    else:
        save({})


@app.command()
def apparate(
    destination: str,
    unsafe: bool = typer.Option(
        False, help="Change the working directory with pure Python."
    ),
):
    """Apparate to the given destination.

    If --unsafe is used, the working directory is changed with pure Python.

    Args:
        destination: [TODO:description]
        safe: [TODO:description]

    Raises:
        typer.Exit: [TODO:description]
        typer.Exit: [TODO:description]
    """
    try:
        data = utils.load_config_data()
    except ConfigError as message:
        if safe:
            print(message)
        else:
            rich.print(message)
        raise typer.Exit(1)

    try:
        path = Path(data[destination])
    except KeyError:
        message = f"Destination '{destination}' is not known!"
        if safe:
            print(message)
        else:
            rich.print(message)
        raise typer.Exit(1)

    if safe:
        cmd = f"cd {path}"
        print(cmd)
    else:
        change_directory(path)


@app.command(hidden=True)
def print_error(message: str):
    rich.print(message, file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    app()
