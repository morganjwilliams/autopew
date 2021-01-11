import shutil
from pathlib import Path
from tempfile import mkdtemp


def temp_path(suffix=""):
    """Return the path of a temporary directory."""
    directory = mkdtemp(suffix=suffix)
    return Path(directory)


def remove_tempdir(directory):
    """
    Remove a specific directory, contained files and sub-directories.

    Parameters
    ----------
    directory: str, Path
        Path to directory.
    """
    directory = Path(directory)
    try:
        shutil.rmtree(str(directory))
        assert not directory.exists()
    except PermissionError:
        pass
