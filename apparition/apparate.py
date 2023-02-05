import fcntl
import shlex
import termios
from pathlib import Path

import click
import typer

from apparition.exceptions import ConfigError
from apparition.io import load_config_data
from apparition.utils import exit_with_error, load


class ApparateCommand(typer.core.TyperCommand):
    """Custom TyperCommand class to modify the usage line."""

    def get_usage(self, ctx: click.Context) -> str:
        """Override get_usage."""
        usage = super().get_usage(ctx)
        if usage.startswith("Usage: apparition apparate"):
            usage = usage.replace("apparition ", "")
        return usage


def safe_apperate(destination: str):
    """Print the change directory path to be evaluated by the shell function."""
    try:
        data = load_config_data()
    except ConfigError as message:
        print(message)
        raise typer.Exit(1)

    try:
        path = data[destination]
    except KeyError as error:
        print(f"Destination '{destination}' is not known!")
        raise typer.Exit(1) from error

    print(f"cd {path}")


def unsafe_apperate(destination: str):
    """Use unsafe_change_directory to change the working directory with pure Python."""
    data = load()

    try:
        path = Path(data[destination])
    except KeyError:
        exit_with_error(f"Destination '{destination}' is not known!")

    unsafe_change_directory(path)


def unsafe_change_directory(path: Path):
    """Change the working directory of the parent shell.

    This is an unsafe hack, the shell command is put back into the TTY.
    If the user types during execution, this can splinch the command.

    Args:
        path: The destination path for the parent shell.
    """
    quoted_path = shlex.quote(str(path))
    backspaces = "\x08" * 32
    command = f"{backspaces}cd {quoted_path}\n"
    for char in command:
        fcntl.ioctl(1, termios.TIOCSTI, str.encode(char))
