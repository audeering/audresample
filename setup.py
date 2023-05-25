import platform
import setuptools


if platform.system() == 'Windows':  # pragma: no cover
    ext_module = 'audresample.core.bin.windows'
    package_data = ['audresample/core/bin/windows/audresample.dll']
elif platform.system() == 'Linux':  # pragma: no cover
    ext_module = 'audresample.core.bin.linux'
    package_data = ['audresample/core/bin/linux/audresample.so']


setuptools.setup(
    # Get versino from git
    use_scm_version=True,
    # Compile platform wheels from pre-compiled binaries
    # https://stackoverflow.com/a/64921892
    has_ext_modules=lambda: True,
    package_data={'audresample': package_data},
    ext_modules=[
        setuptools.Extension(
            name=ext_module,
            sources=[],
        )
    ],
)
