"""
This module provides the DummyPackageTester class for testing the DummyPackage class.
"""
import os.path
from importlib import import_module
from dummy_package_manager import DummyPackage


class DummyPackageTester:
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
        if not requirements:
            requirements = []
        self.dummy_package = DummyPackage(package_name, requirements=requirements, temp_dir=temp_dir)
        self.package = None

    def __enter__(self):
        """
        Context manager enter method.
        Creates the dummy package and its optional dependencies if any, and initializes the package attribute.
        """
        self.dummy_package.__enter__()
        self.package = self._create_dummy_package_tester()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit method.
        Uninstalls the dummy package and its optional dependencies, and cleans up temporary directory.
        """
        self.dummy_package.__exit__(exc_type, exc_val, exc_tb)

    def _create_dummy_package_tester(self):
        """
        Create the dummy package and return its attributes.

        Returns:
            dict: A dictionary representing the dummy package and its dependencies.
        """
        return self.dummy_package.package

    def install_tester(self):
        """
        Install the dummy package and optional dependencies using pip, and verify installation.

        Returns:
            bool: True if installation is successful, False otherwise.
        """
        self.dummy_package.install()
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
        self.dummy_package.uninstall()
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
    is_path = os.path.exists(tester.dummy_package.temp_dir)
    is_module = None
    try:
        main_module = import_module(tester.dummy_package.package["name"])
        dep_modules = False
        if tester.dummy_package.package["deps"] is not []:
            dep_modules = [import_module(deps["name"]) for deps in tester.dummy_package.package["deps"]]
        is_module = not main_module and not dep_modules
    except ImportError:
        is_module = True
    return not is_path and is_module
