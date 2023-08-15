"""
This module provides the DummyPackageTester class for testing the DummyPackage class.
"""
from importlib import import_module
from unittest.mock import Mock
from dummy_package_manager import DummyPackage


class DummyPackageTester(DummyPackage):
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
        self.mock = Mock()
        self.mock.__exit__ = Mock(return_value=False)

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
