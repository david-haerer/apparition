from pathlib import Path

import yaml
from appdirs import user_config_dir

from apparition.exceptions import ConfigError


def get_config_path() -> Path:
    """Return the platform specific config path for the app.

    Returns:
        Path: The platform specific config path.
    """
    app_name = "apparition"
    config_path = Path(user_config_dir(app_name)) / "config.yml"
    return config_path


def load_config_data() -> dict[str, Path]:
    """Load the app data.

    Returns:
        dict[str, Path]: The app data.

    Raises:
        ConfigError: If the config file is invalid.
    """
    config_path = get_config_path()
    if not config_path.is_file():
        return {}
    try:
        with open(config_path, "r", encoding="utf-8") as file:
            rawdata = yaml.safe_load(file)
    except yaml.scanner.ScannerError as error:
        raise ConfigError(f"Failed to read '{config_path}'!") from error
    if rawdata is None:
        return {}
    data = {alias: Path(path) for alias, path in rawdata.items()}
    return data


def save_config_data(data: dict[str, Path]):
    """Save the app data.

    Args:
        data: The app data to save.

    Raises:
        ConfigError: If the parent of the config path is a file (must be a directory).
    """
    config_path = get_config_path()
    if config_path.parent.is_file():
        raise ConfigError(f"'{config_path.parent}' is a file but must be a directory!")
    if not config_path.parent.exists():
        config_path.parent.mkdir(parents=True)
    raw_data = {alias: str(path.resolve()) for alias, path in data.items()}
    with open(config_path, mode="wt", encoding="utf-8") as file:
        yaml.dump(raw_data, file)


def load_shell_function() -> list[str]:
    """Return the lines of the resources/apparate.sh function.

    Returns:
        list[str]: The lines of the file (without trailing newline).
    """
    path = Path(__file__).parent / "resources" / "apparate.sh"
    with open(path, "r", encoding="utf-8") as file:
        lines = [line[:-1] for line in file.readlines()]
    return lines
