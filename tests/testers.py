"""
This module provides the DummyPackageTester class for testing the DummyPackage class.
"""

import os.path
from importlib import import_module
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


def __exit___tester(tester):
    """
    Verify the cleanup of the package's temporary directory and its module(s) after exiting the context.

    Args:
        tester (DummyPackageTester): The DummyPackageTester instance representing the package tester to be verified.

    Returns:
        bool: True if the package's temporary directory and module(s) are cleaned up, False otherwise.
    """
    is_path = os.path.exists(tester.temp_dir)
    is_module = False
    try:
        main_module = import_module(tester.package["name"])
        dep_modules = False
        if tester.package["deps"]:
            dep_modules = any(import_module(deps["name"]) for deps in tester.package["deps"])
        is_module = main_module or dep_modules
    except ImportError:
        is_module = False
    return not is_path and not is_module
