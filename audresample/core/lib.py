import ctypes
import os
import platform


def platform_name():
    r"""Platform name used in pip tag.

    Expected outcomes are:

    ==================== ======================
    Linux, 64-bit        manylinux_2_17_x86_64
    Raspberry Pi, 32-bit manylinux_2_17_armv7l
    Raspberry Pi, 64-bit manylinux_2_17_aarch64
    Windows              win_amd64
    MacOS Intel          macosx_10_4_x86_64
    MacOS M1             macosx_11_0_arm64
    ==================== ======================

    Under Linux the manylinux version
    can be extracted
    by inspecting the wheel
    with ``auditwheel``.

    Too see all supported tags on your system run:

    .. code-block:: bash

        $ pip debug --verbose

    """
    system = platform.system()
    machine = platform.machine().lower()

    if system == "Linux":  # pragma: no cover
        system = "manylinux_2_17"
    elif system == "Windows":  # pragma: no cover
        system = "win"
    elif system == "Darwin":  # pragma: no cover
        if machine == "x86_64":
            system = "macosx_10_4"
        else:
            system = "macosx_11_0"
    else:  # pragma: no cover
        raise RuntimeError(f"Unsupported platform {system}")

    return f"{system}_{machine}"


# load library

root = os.path.dirname(os.path.realpath(__file__))
bin_path = os.path.join(root, "bin")

plat_name = platform_name()

if "linux" in plat_name:  # pragma: no cover
    library = "libaudresample.so"
elif "macos" in plat_name:  # pragma: no cover
    library = "libaudresample.dylib"
elif "win" in plat_name:  # pragma: no cover
    library = "audresample.dll"

lib_path = os.path.join(bin_path, plat_name, library)

lib = ctypes.cdll.LoadLibrary(lib_path)


# resample


class ConverterConfig(ctypes.Structure):  # noqa: D101
    _fields_ = [
        ("srIn", ctypes.c_double),
        ("srOut", ctypes.c_double),
        ("quality", ctypes.c_char),
    ]


lib.init_converter_config.argtypes = [
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_char,
]
lib.init_converter_config.restype = ConverterConfig

lib.get_output_length.argtypes = [
    ctypes.c_size_t,
    ConverterConfig,
]
lib.get_output_length.restype = ctypes.c_size_t

lib.audresample_oneshot.argtypes = [
    ConverterConfig,
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_size_t,
]
lib.audresample_oneshot.restype = None

lib.do_mono_mixdown.argtypes = [
    ctypes.POINTER(ctypes.c_float),
    ctypes.POINTER(ctypes.c_float),
    ctypes.c_size_t,
    ctypes.c_uint,
]
lib.do_mono_mixdown.restype = None
