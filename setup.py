import platform
import setuptools

# Include only the platform specific pre-compiled binary.
# For sources see https://github.com/audeering/audresamplelib

# Linux
if platform.system() == 'Linux':
    path = 'linux/*.so'
    plat_name = 'manylinux_x86_64'

# Windows
elif platform.system() == 'Windows':
    path = 'windows/*.dll'
    plat_name = 'win_amd64'

# MacOS Intel
elif (
        platform.system() == 'Darwin'
        and platform.processor() == 'i386'
):
    path = 'macos-intel/*.dylib'
    plat_name = 'macosx_x86_64'

# MacOS M1
elif (
        platform.system() == 'Darwin'
        and platform.processor() == 'arm'
):
    path = 'macos-m1/*.dylib'
    plat_name = 'macosx_arm64'

else:
    raise RuntimeError('Unsupported platform')


setuptools.setup(
    use_scm_version=True,
    packages=setuptools.find_packages(),
    package_data={
        'audresample.core': [f'bin/{path}']
    },
    # python -m build --wheel
    # does no longer accept the --plat-name option,
    # but we can set the desired platform as an option
    # (https://stackoverflow.com/a/75010995)
    options={
        'bdist_wheel': {'plat_name': plat_name},
    },
)
