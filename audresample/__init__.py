from audresample.core import define
from audresample.core.api import (
    am_fm_synth,
    remix,
    resample,
)
from audresample.core.config import config


__all__ = []


# Dynamically get the version of the installed module
try:
    import pkg_resources
    __version__ = pkg_resources.get_distribution(__name__).version
except Exception:  # pragma: no cover
    pkg_resources = None  # pragma: no cover
finally:
    del pkg_resources
