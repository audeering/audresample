from doctest import ELLIPSIS
from doctest import NORMALIZE_WHITESPACE

import matplotlib

# Use a non-interactive backend to avoid opening windows during doctests
matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from sybil import Sybil  # noqa: E402
from sybil.parsers.rest import DocTestParser  # noqa: E402
from sybil.parsers.rest import PythonCodeBlockParser  # noqa: E402

import audresample  # noqa: E402
import audresample.define  # noqa: E402, F401


def plot_signal(signal, sampling_rate):
    """Plot audio signal (used inside usage.rst doctests)."""
    num_channels = signal.shape[0]
    num_samples = signal.shape[1]
    plt.rcParams["figure.figsize"] = [12, 2 * num_channels]
    t = np.linspace(0, num_samples / sampling_rate, num_samples)
    if num_channels > 1:
        fig, axs = plt.subplots(nrows=num_channels)
        for ax, channel in zip(axs, signal):
            ax.plot(t, channel)
            ax.set_xlabel("Time / s")
            ax.set_ylabel("Magnitude")
            ax.set_ylim([-1, 1])
    else:
        plt.plot(t, signal.squeeze())
        plt.xlabel("Time / s")
        plt.ylabel("Magnitude")
        plt.ylim([-1, 1])
    plt.tight_layout()


def imports(namespace):
    """Provide modules and helpers to the doctest namespace."""
    namespace["audresample"] = audresample
    namespace["plot_signal"] = plot_signal


# Collect doctests
pytest_collect_file = Sybil(
    parsers=[
        DocTestParser(optionflags=ELLIPSIS | NORMALIZE_WHITESPACE),
        PythonCodeBlockParser(),
    ],
    patterns=["usage.rst"],
    setup=imports,
).pytest()
