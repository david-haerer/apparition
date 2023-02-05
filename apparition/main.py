import sys
from pathlib import Path

import rich
import typer

from apparition.apparate import ApparateCommand, safe_apperate, unsafe_apperate
from apparition.io import load_shell_function
from apparition.utils import (
    check_platform,
    exit_with_error,
    get_shell_config_file,
    load,
    save,
)

check_platform()
SHELLRC = get_shell_config_file()

app = typer.Typer()
console = rich.console.Console()


@app.command(
    help=(
        f"🪄 Add the output of this command to your '{SHELLRC}'.\n\n"
        f"You can do this by running 'apparition install >> {SHELLRC}'. "
        f"Then run 'source {SHELLRC}'.\n\n"
        "This creates a shell function called 'apparate' "
        "that can change the working directory in a safe manner."
    )
)
def install():
    """Help text in the @app.command() to display the correct shellrc."""
    shell_function = load_shell_function()
    for line in shell_function:
        rich.print(line)


@app.command()
def set(
    destination: str = typer.Argument(..., help="The name of the destination."),
    path: Path = typer.Argument(..., help="The path to the destination."),
):
    """✨ Set a new destination.

    This command can also be used to update an existing destination.
    """
    data = load()
    data[destination] = path
    save(data)
    data = load()
    rich.print(f"✨ [bold]{destination}:[/bold] {data[destination]}")


@app.command()
def remove(
    destination: str = typer.Argument(..., help="Name of the destination to remove.")
):
    """🗑️ Remove a destination."""
    data = load()
    try:
        del data[destination]
    except KeyError:
        exit_with_error(f"Destination '{destination}' is unknown.")
    save(data)
    rich.print(f"🗑️ [bold]{destination}[/bold]")


@app.command()
def rename(
    old_name: str = typer.Argument(..., help="Old name of the destination."),
    new_name: str = typer.Argument(..., help="New name of the destination."),
):
    """✍️ Rename a destination."""
    data = load()
    data[new_name] = data[old_name]
    del data[old_name]
    save(data)
    rich.print(f"✍️ [bold]{old_name}[/bold] → [bold]{new_name}[/bold]")


@app.command()
def show(
    list_style: bool = typer.Option(False, "--list", help="Show the output in list format."),
    destination: str = typer.Argument(None, help="Only show the path to this destination."),
):
    """📜 Show all destinations.
    
    By default it will show the output in table format.
    """
    data = load()
    if destination is not None:
        try:
            path = Path(data[destination])
        except KeyError:
            exit_with_error(f"Destination '{destination}' is not known!")
        rich.print(path)
        return

    if list_style:
        for dest in sorted(data.keys()):
            path = data[dest]
            rich.print(f"[bold]{dest}:[/bold] {str(path.resolve())}")
    else:
        table = rich.table.Table("Destination", "Path")
        for dest in sorted(data.keys()):
            path = data[dest]
            table.add_row(dest, str(path.resolve()))
        console.print(table)


@app.command()
def check():
    """✔️ Check that the path to each destination is a directory."""
    data = load()

    if len(data) == 0:
        rich.print("ℹ️ There are no destinations to check.")
        return

    no_errors : bool = True
    for destination, path in data.items():
        if not path.is_dir():
            if no_errors:
                rich.print("❌ The following destinations don't lead to a directory:")
            rich.print(f"[bold]{destination}:[/bold] {path}")
            no_errors = False

    if no_errors:
        rich.print("✔️ All destinations lead to a directory.")
        return

    raise typer.Exit(1)



@app.command()
def purge():
    """🔥 Remove all destinations.

    The command asks for confirmation if you are sure.
    """
    typer.confirm("Are you sure you want to delete all destinations?", abort=True)
    save({})
    rich.print("🔥 Removed all destinations.")


@app.command(cls=ApparateCommand)
def apparate(
    destination: str = typer.Argument(..., help="The name of the destination."),
    called_from_shell_function: bool = typer.Option(False, hidden=True),
    unsafe: bool = typer.Option(False, hidden=True),
):
    """🌀 Apparate to the given destination."""
    if not unsafe and not called_from_shell_function:
        exit_with_error(
            "This command has to be called from the shell function!\n"
            "Refer to 'appparition install --help'."
        )

    if unsafe:
        unsafe_apperate(destination)
    else:
        safe_apperate(destination)


@app.command(hidden=True)
def print_error(message: str):
    """Print the given error message and exit with a non-zero status code."""
    rich.print(f"[bold red]Error:[/bold red] {message}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    app()
