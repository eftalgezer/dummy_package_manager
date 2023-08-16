"""
Main test module for the dummy package manager.

This module runs the main test function `test_DummyPackage()` from the `tests` module.
It checks the functionality of the DummyPackage class using various scenarios.
"""

from .tests import test_DummyPackage, test_DummyPackage__errors

if __name__ == "__main__":
    test_DummyPackage()
    test_DummyPackage__errors()
