from pathlib import Path

import pytest
from typer.testing import CliRunner

from apparition.main import app

runner = CliRunner(mix_stderr=False)


@pytest.fixture
def apparate_sh():
    path = Path(__file__).parent.parent / "resources" / "apparate.sh"
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    return content


def test_install(apparate_sh):
    result = runner.invoke(app, ["install"])
    assert result.exit_code == 0
    assert apparate_sh in result.stdout


def test_install_help():
    result = runner.invoke(app, ["install", "--help"])
    print(result.stdout)
    assert result.exit_code == 0
    assert "Add the output of this command to your '~/.bashrc'." in result.stdout
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
    mocked_load = mocker.patch(
        "apparition.main.load",
        side_effect=[
            {},
            {
                "hogwarts": "/path/to/hogwarts",
            },
        ],
    )
    mocked_save = mocker.patch("apparition.main.save")
    result = runner.invoke(app, ["set", "hogwarts", "/path/to/hogwarts"])
    assert result.exit_code ==  0
    assert "✨ hogwarts: /path/to/hogwarts" in result.stdout


def test_set_help():
    result = runner.invoke(app, ["set", "--help"])
    print(result.stdout)
    assert result.exit_code == 0
    assert "Set a new destination." in result.stdout
    assert "This command can also be used to update an existing destination." in result.stdout


def test_set(mocker):
    mocked_load = mocker.patch(
        "apparition.main.load",
        side_effect=[
            {},
            {
                "hogwarts": "/path/to/hogwarts",
            },
        ],
    )
    mocked_save = mocker.patch("apparition.main.save")
    result = runner.invoke(app, ["set", "hogwarts", "/path/to/hogwarts"])
    assert result.exit_code == 0
    assert "✨ hogwarts: /path/to/hogwarts" in result.stdout


def test_set_help():
    result = runner.invoke(app, ["set", "--help"])
    print(result.stdout)
    assert result.exit_code == 0
    assert "Set a new destination." in result.stdout
    assert "This command can also be used to update an existing destination." in result.stdout