"""Run Buildozer with compatibility fixes for Python 3.12+.

This script ensures the deprecated ``distutils`` module is available to
Buildozer by providing it from ``setuptools`` when running under
Python 3.12 or newer.
"""

import sys

try:
    # Preload distutils from setuptools for Python 3.12+
    import distutils  # noqa: F401
except ModuleNotFoundError:
    import setuptools
    sys.modules['distutils'] = setuptools._distutils

from buildozer.scripts.client import main

if __name__ == "__main__":
    sys.exit(main())
