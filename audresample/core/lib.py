import ctypes
import os
import platform


# load library

root = os.path.dirname(os.path.realpath(__file__))

bin_path = os.path.join(root, 'bin')
if platform.system() == 'Windows':  # pragma: no cover
    # for some reason we have to load soxr.dll first...
    lib_path = os.path.join(bin_path, 'soxr.dll')
    ctypes.cdll.LoadLibrary(lib_path)
    lib_path = os.path.join(bin_path, 'audresample.dll')
elif platform.system() == 'Linux':  # pragma: no cover
    lib_path = os.path.join(bin_path, 'libaudresample.so')
elif platform.system() == 'Darwin':  # pragma: no cover
    lib_path = os.path.join(bin_path, 'libaudresample.dylib')
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
