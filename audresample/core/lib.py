import ctypes
import os
import platform


def platform_name():

    # Extract platform name from system + processor
    system = platform.system()
    processor = platform.processor()

    if system == 'Linux' and processor == 'x86_64':
        # That we support 2_17 can be seen
        # when inspecting the wheel with auditwheel
        plat_name = 'manylinux_2_17_x86_64'

    elif system == 'Windows':
        plat_name = 'win_amd64'

    elif system == 'Darwin' and processor == 'i386':
        plat_name = 'macosx_12_0_x86_64'

    elif system == 'Darwin' and processor == 'arm':
        plat_name = 'macosx_12_0_arm64'

    else:
        raise RuntimeError(
            f'Unsupported platform {system}-{processor}'
        )

    return plat_name


# load library

root = os.path.dirname(os.path.realpath(__file__))
plat_name = platform_name()
bin_path = os.path.join(root, 'bin')

if plat_name == 'win_amd64':  # pragma: no cover
    lib_path = os.path.join(bin_path, 'windows', 'audresample.dll')

elif plat_name == 'manylinux_2_17_x86_64':  # pragma: no cover
    lib_path = os.path.join(bin_path, 'linux', 'libaudresample.so')

elif plat_name == 'macosx_12_0_x86_64':  # pragma: no cover
    lib_path = os.path.join(bin_path, 'macos-intel', 'libaudresample.dylib')

elif plat_name == 'macosx_12_0_arm64':  # pragma: no cover
    lib_path = os.path.join(bin_path, 'macos-m1', 'libaudresample.dylib')

else:  # pragma: no cover
    raise RuntimeError("Unsupported platform")

lib = ctypes.cdll.LoadLibrary(lib_path)


# resample

class ConverterConfig(ctypes.Structure):
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
