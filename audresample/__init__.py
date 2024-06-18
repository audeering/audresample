from audresample.core import define
from audresample.core.api import am_fm_synth
from audresample.core.api import remix
from audresample.core.api import resample
from audresample.core.config import config


__all__ = []


# Dynamically get the version of the installed module
try:
    import importlib.metadata

    __version__ = importlib.metadata.version(__name__)
except Exception:  # pragma: no cover
    importlib = None  # pragma: no cover
finally:
    del importlib
