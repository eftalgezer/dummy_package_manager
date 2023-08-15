"""
This module provides the DummyPackageTester class for testing the DummyPackage class.
"""
from importlib import import_module
from unittest import TestCase
from dummy_package_manager import DummyPackage


class DummyPackageTester(TestCase, DummyPackage):
    """
    A class for testing the DummyPackage class and its functionality.

    Args:
        package_name (str): The name of the dummy package to test.
        requirements (list): A list of package names for optional dependencies.
        temp_dir (str): Temporary directory path to use for package creation.
    """

    def __init__(self, package_name, requirements=None, temp_dir=None):
        """
        Initialize a DummyPackageTester instance.

        Args:
            package_name (str): The name of the dummy package to test.
            requirements (list, optional): A list of package names for optional dependencies.
            temp_dir (str, optional): Temporary directory path to use for package creation.
        """
        super().__init__(package_name, requirements, temp_dir)

    def setUp(self) -> None:
        self.v = setup_with_context_manager(self, DummyPackage)

    def install_tester(self):
        """
        Install the dummy package and optional dependencies using pip, and verify installation.

        Returns:
            bool: True if installation is successful, False otherwise.
        """
        self.install()
        try:
            main_module = import_module(self.package["name"])
            dep_modules = True
            if self.package["deps"] is not []:
                dep_modules = [import_module(deps["name"]) for deps in self.package["deps"]]
            return main_module and dep_modules
        except ImportError:
            return False

    def uninstall_tester(self):
        """
        Uninstall the dummy package and optional dependencies using pip, and verify uninstallation.

        Returns:
            bool: True if uninstallation is successful, False otherwise.
        """
        self.uninstall()
        try:
            main_module = import_module(self.package["name"])
            dep_modules = False
            if self.package["deps"] is not []:
                dep_modules = [import_module(deps["name"]) for deps in self.package["deps"]]
            return not main_module and not dep_modules
        except ImportError:
            return True


def setup_with_context_manager(testcase, cm):
    """Use a contextmanager to setUp a test case."""
    val = cm.__enter__()
    testcase.addCleanup(cm.__exit__, None, None, None)
    return val
