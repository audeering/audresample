import os
import platform

import setuptools


# Include only the platform specific pre-compiled binary.
# For sources see https://github.com/audeering/audresamplelib


def platform_name():
    r"""Platform name used in pip tag.

    Expected outcomes are:

    ==================== ======================
    Linux, 64-bit        manylinux_2_17_x86_64
    Raspberry Pi, 32-bit manylinux_2_17_armv7l
    Raspberry Pi, 64-bit manylinux_2_17_aarch64
    Windows              win_amd64
    MacOS Intel          macosx_12_0_x86_64
    MacOS M1             macosx_12_0_arm64
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
    system_mapping = {
        'Linux': 'manylinux_2_17',
        'Windows': 'win',
        'Darwin': 'macosx_12_0',
    }

    if system not in system_mapping:
        raise RuntimeError(f'Unsupported platform {system}')

    return f'{system_mapping[system]}_{machine}'


# Look for enrionment variable PLAT_NAME
# to be able to enforce
# different platform names
# in CI on the same runner
plat_name = os.environ.get('PLAT_NAME', platform_name())

if 'linux' in plat_name:
    library = '*.so'
elif 'macos' in plat_name:
    library = '*.dylib'
elif 'win' in plat_name:
    library = '*.dll'

setuptools.setup(
    use_scm_version=True,
    packages=setuptools.find_packages(),
    package_data={
        'audresample.core': [f'bin/{plat_name}/{library}']
    },
    # python -m build --wheel
    # does no longer accept the --plat-name option,
    # but we can set the desired platform as an option
    # (https://stackoverflow.com/a/75010995)
    options={
        'bdist_wheel': {'plat_name': plat_name},
    },
)
