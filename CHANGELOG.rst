Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_,
and this project adheres to `Semantic Versioning`_.


Version 1.2.1 (2023-01-27)
--------------------------

* Fixed: require ``sphinx-audeering-theme>=1.2.1``
  to ensure the correct theme is used
  for the public documentation


Version 1.2.0 (2023-01-27)
--------------------------

* Added: support for MacOS M1 architecture


Version 1.1.1 (2022-12-23)
--------------------------

* Added: support for Python 3.11
* Added: support for Python 3.10
* Changed: split API documentation into sub-pages
  for each function
* Fixed: missing ``__init__.py`` file for
  ``audresample.define``


Version 1.1.0 (2022-02-03)
--------------------------

* Added: support for non single precision floating-point formats
  in ``audresample.remix()``
* Changed: raise a ``RuntimeError`` in ``audresample.resample()``
  when a non single precision floating-point input signal is given
  instead of converting it silently


Version 1.0.0 (2022-01-04)
--------------------------

* Added: Python 3.9 support
* Removed: Python 3.6 support


Version 0.1.6 (2021-06-17)
--------------------------

* Added: Windows support


Version 0.1.5 (2021-05-10)
--------------------------

* Added: macOS support


Version 0.1.4 (2021-03-26)
--------------------------

* Fixed: "Edit on Github" link in the docs


Version 0.1.3 (2021-03-25)
--------------------------

* Changed: move to Github and release as open source


Version 0.1.2 (2021-03-18)
--------------------------

* Added: ``upmix`` argument to ``remix()``


Version 0.1.1 (2021-01-15)
--------------------------

* Fixed: Updating binaries to RELEASE versions (execution time greatly reduced!)


Version 0.1.0 (2020-02-12)
--------------------------

* Added: Initial release


.. _Keep a Changelog: https://keepachangelog.com/en/1.0.0/
.. _Semantic Versioning: https://semver.org/spec/v2.0.0.html
