import sys
from pathlib import Path
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


def autopew_datafolder(subfolder=None):
    """
    Returns the path of the autopew data folder.

    Parameters
    -----------
    subfolder : :class:`str`
        Subfolder within the autopew data folder.

    Returns
    -------
    :class:`pathlib.Path`
    """
    pth = Path(sys.modules["autopew"].__file__).parent / "data"
    if subfolder:
        pth /= subfolder
    return pth
