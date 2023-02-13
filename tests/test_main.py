# pylint: disable=no-member

import fcntl
import termios
from pathlib import Path
from unittest.mock import call, ANY

import yaml

from typer.testing import CliRunner

import apparition
from apparition.main import app

runner = CliRunner(mix_stderr=False)


def test_install():
    """Test the install command."""
    path = Path(__file__).parent.parent / "apparition" / "resources" / "apparate.sh"
    with open(path, "r", encoding="utf-8") as file:
        apparate_sh = file.read()

    result = runner.invoke(app, ["install"])

    assert result.exit_code == 0
    assert apparate_sh in result.stdout


def test_install_help():
    """Test the help of the install command."""
    result = runner.invoke(app, ["install", "--help"])

    assert result.exit_code == 0
    assert "🪄 Add the output of this command to your '~/.bashrc'." in result.stdout
    assert (
        "You can do this by running 'apparition install >> ~/.bashrc'. Then run 'source"
        in result.stdout
    )
    assert "~/.bashrc'." in result.stdout
    assert (
        "This creates a shell function called 'apparate' that can change the working"
        in result.stdout
    )
    assert "directory in a safe manner." in result.stdout


def test_set(mocker):
    """Test the set command."""
    mocker.patch("yaml.safe_load", side_effect=[{}, {"hogwarts": "/path/to/hogwarts"}])
    mocker.patch("yaml.dump")

    result = runner.invoke(app, ["set", "hogwarts", "/path/to/hogwarts"])

    assert result.exit_code == 0
    assert "✨ hogwarts: /path/to/hogwarts" in result.stdout
    yaml.dump.assert_called_once_with({"hogwarts": "/path/to/hogwarts"}, ANY)


def test_set_help():
    """Test the help of the set command."""
    result = runner.invoke(app, ["set", "--help"])

    assert result.exit_code == 0
    assert "✨ Set a new destination." in result.stdout
    assert (
        "This command can also be used to update an existing destination."
        in result.stdout
    )
    assert "The name of the destination." in result.stdout
    assert "The path to the destination." in result.stdout


def test_remove(mocker):
    """Test the remove command."""
    mocker.patch("yaml.safe_load", return_value={"hogwarts": "/path/to/hogwarts"})
    mocker.patch("yaml.dump")

    result = runner.invoke(app, ["remove", "hogwarts"])

    assert result.exit_code == 0
    assert "🗑️ hogwarts" in result.stdout
    yaml.dump.assert_called_once_with({}, ANY)


def test_remove_help():
    """Test the help of the remove command."""
    result = runner.invoke(app, ["remove", "--help"])

    assert result.exit_code == 0
    assert "🗑️ Remove a destination." in result.stdout
    assert "Name of the destination to remove." in result.stdout


def test_rename(mocker):
    """Test the rename command."""
    mocker.patch("yaml.safe_load", return_value={"hogwarts": "/path/to/hogwarts"})
    mocker.patch("yaml.dump")

    result = runner.invoke(app, ["rename", "hogwarts", "school"])

    assert result.exit_code == 0
    assert "✍️ hogwarts → school" in result.stdout
    yaml.dump.assert_called_once_with({"school": "/path/to/hogwarts"}, ANY)


def test_rename_help():
    """Test the help of the rename command."""
    result = runner.invoke(app, ["rename", "--help"])

    assert result.exit_code == 0
    assert "✍️ Rename a destination." in result.stdout
    assert "Old name of the destination." in result.stdout
    assert "New name of the destination." in result.stdout


def test_show_all_table(mocker):
    """Test the show command for all destinations in table format."""
    mocker.patch("yaml.safe_load", return_value={
        "hogwarts": "/path/to/hogwarts",
        "azkaban": "/path/to/azkaban",
    })
    mocker.patch("yaml.dump")

    result = runner.invoke(app, ["show"])

    assert result.exit_code == 0
    assert "┃ Destination ┃ Path              ┃" in result.stdout
    assert "│ azkaban     │ /path/to/azkaban  │" in result.stdout
    assert "│ hogwarts    │ /path/to/hogwarts │" in result.stdout


def test_show_all_list(mocker):
    """Test the show command for all destinations in list format."""
    mocker.patch("yaml.safe_load", return_value={
        "hogwarts": "/path/to/hogwarts",
        "azkaban": "/path/to/azkaban",
    })
    mocker.patch("yaml.dump")

    result = runner.invoke(app, ["show", "--list"])

    assert result.exit_code == 0
    assert "azkaban: /path/to/azkaban" in result.stdout
    assert "hogwarts: /path/to/hogwarts" in result.stdout


def test_show_single_destination(mocker):
    """Test the show command for a single destination."""
    mocker.patch("yaml.safe_load", return_value={
        "hogwarts": "/path/to/hogwarts",
        "azkaban": "/path/to/azkaban",
    })
    mocker.patch("yaml.dump")

    result = runner.invoke(app, ["show", "hogwarts"])

    assert result.exit_code == 0
    assert "│ hogwarts    │ /path/to/hogwarts │" not in result.stdout
    assert "hogwarts: /path/to/hogwarts" not in result.stdout
    assert "/path/to/hogwarts" in result.stdout


def test_show_help():
    """Test the help of the show command."""
    result = runner.invoke(app, ["show", "--help"])

    assert result.exit_code == 0
    assert "📜 Show all destinations." in result.stdout
    assert "By default it will show the output in table format." in result.stdout
    assert "Show the output in list format." in result.stdout
    assert "Only show the path to this destination." in result.stdout


def test_check(mocker):
    """Test the check command."""
    mocker.patch("yaml.safe_load", return_value={"hogwarts": "/path/to/hogwarts"})
    mocker.patch("yaml.dump")

    result = runner.invoke(app, ["check"])

    assert result.exit_code == 1
    assert "❌ The following destinations don't lead to a directory:" in result.stdout
    assert "hogwarts: /path/to/hogwarts" in result.stdout


def test_check_help():
    """Test the help of the check command."""
    result = runner.invoke(app, ["check", "--help"])

    assert result.exit_code == 0
    assert "✔️ Check that the path to each destination is a directory." in result.stdout


def test_purge(mocker):
    """Test the purge command."""
    mocker.patch("yaml.dump")

    result = runner.invoke(app, ["purge"], input="y\n")

    assert result.exit_code == 0
    assert "🔥 Removed all destinations." in result.stdout
    yaml.dump.assert_called_once_with({}, ANY)


def test_purge_help():
    """Test the help of the purge command."""
    result = runner.invoke(app, ["purge", "--help"])

    assert result.exit_code == 0
    assert "🔥 Remove all destinations." in result.stdout
    assert "The command asks for confirmation if you are sure." in result.stdout


def test_apparate(mocker):
    """Test the apparate command safe and not called from the shell function."""
    mocker.patch("yaml.safe_load", return_value={"hogwarts": "/path/to/hogwarts"})

    result = runner.invoke(app, ["apparate", "hogwarts"])

    assert result.exit_code == 1
    assert (
        "Error: This command has to be called from the shell function!" in result.stderr
    )
    assert "Refer to 'appparition install --help'." in result.stderr


def test_apparate_called_from_shell_function(mocker):
    """Test the apparate command safe and called from the shell function."""
    mocker.patch("yaml.safe_load", return_value={"hogwarts": "/path/to/hogwarts"})

    result = runner.invoke(
        app, ["apparate", "hogwarts", "--called-from-shell-function"]
    )

    assert result.exit_code == 0
    assert "cd /path/to/hogwarts" in result.stdout


def test_apparate_unsafe(mocker):
    """Test the apparate command unsafe."""
    mocker.patch("yaml.safe_load", return_value={"hogwarts": "/path/to/hogwarts"})
    mocker.patch("apparition.apparate.fcntl.ioctl")

    result = runner.invoke(app, ["apparate", "hogwarts", "--unsafe"])

    backspaces = "\x08" * 32
    command = backspaces + "cd /path/to/hogwarts\n"
    expected_calls = [call(1, termios.TIOCSTI, str.encode(char)) for char in command]

    assert result.exit_code == 0
    assert fcntl.ioctl.mock_calls == expected_calls


def test_apparate_help():
    """Test the help of the apparate command unsafe."""
    result = runner.invoke(app, ["apparate", "--help"])

    assert result.exit_code == 0
    assert "🌀 Apparate to the given destination." in result.stdout
    assert "The name of the destination." in result.stdout
