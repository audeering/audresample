from setuptools import setup


setup(
    # Get versino from git
    use_scm_version=True,
    # Compile platform wheels from pre-compiled binaries
    has_ext_modules=lambda: True,
)
