import os
import sys
from pathlib import Path

import rich

from apparition.exceptions import ConfigError
from apparition.io import load_config_data, save_config_data


def exit_with_error(message):
    """Print an error message and exit with a non-zero status code.

    Args:
        message: The error message.
    """
    rich.print(f"[bold red]Error:[/bold red] {message}", file=sys.stderr)
    sys.exit(1)


def save(data: dict[str, Path]):
    """Wrap save_config_data() and use exit_with_error() on ConfigError."""
    try:
        save_config_data(data)
    except ConfigError as message:
        exit_with_error(message)


def load() -> dict[str, Path]:
    """Wrap load_config_data() and use utils.exit_with_error() on ConfigError."""
    try:
        data = load_config_data()
    except ConfigError as message:
        exit_with_error(message)
    return data


def check_platform():
    """Check if the platform is supported or exit with an error."""
    platform = sys.platform
    if platform in ("linux", "linux2"):
        return
    if platform == "darwin":
        exit_with_error("macOS is not supported!")
    if platform == "win32":
        exit_with_error("Windows is not supported!")
    exit_with_error("Unknown OS!")


def get_shell_config_file() -> str:
    """Return the path to the config file of the users shell.

    Returns:
        str: The path to the config file.
    """
    shell = os.environ["SHELL"]
    if "zsh" in shell:
        return "~/.zshrc"
    return "~/.bashrc"
