"""
This module provides the DummyPackage class which allows creating and managing dummy Python packages with optional
dependencies.

"""

import os
import tempfile
import shutil
from subprocess import run
from shlex import split


class DummyPackage:
    """
    A class to create and manage dummy Python packages with optional dependencies.

    Args:
        package_name (str): The name of the dummy package.
        requirements (list): A list of package names for optional dependencies.
        temp_dir (str): Temporary directory path to use for package creation.
    """

    def __init__(self, package_name, requirements=None, temp_dir=None):
        """
        Initialize a DummyPackage instance.

        Args:
            package_name (str): The name of the dummy package.
            requirements (list): A list of package names for optional dependencies.
            temp_dir (str, optional): Temporary directory path to use for package creation.
                                      If not provided, a temporary directory will be created.
        """
        if not requirements:
            requirements = []
        self.package_name = package_name
        self.requirements = requirements
        self.temp_dir = temp_dir
        self.package = None

    def __enter__(self):
        """
        Context manager enter method.
        Creates the dummy package and its optional dependencies if any.
        """
        if self.temp_dir is None:
            self.temp_dir = tempfile.mkdtemp()
        self.package = self._create_dummy_package()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit method.
        Uninstalls the dummy package and its optional dependencies and cleans up temporary directory.
        """
        self.uninstall()
        shutil.rmtree(self.temp_dir)

    def _create_dummy_package(self):
        """
        Create the dummy package and optional dependencies.

        Returns:
            dict: A dictionary representing the dummy package and its dependencies.
        """
        package = {
            "name": self.package_name,
            "source_dir": None,
            "deps": [
                {
                    "name": requirement,
                    "source_dir": None
                }
                for requirement in self.requirements
            ]
        }
        for dep in package["deps"]:
            index = package["deps"].index(dep)
            package["deps"][index]["source_dir"] = os.path.join(self.temp_dir, package["deps"][index]["name"])
            os.makedirs(package["deps"][index]["source_dir"])
            init_file = os.path.join(
                package["deps"][index]["source_dir"],
                package["deps"][index]["name"],
                "__init__.py"
            )
            with open(init_file, "w", encoding="utf-8"):
                pass
            setup_content = "from setuptools import setup, find_packages\n\n" \
                            "requirements = {self.requirements!r} if {self.requirements!r} else []\n" \
                            "setup(\n" \
                            "    name='{package_name}',\n" \
                            "    version='0.1.0',\n" \
                            "    packages=find_packages(),\n" \
                            "    install_requires=requirements\n" \
                            ")\n"
            setup_file = os.path.join(package["deps"][index]["source_dir"], "setup.py")
            with open(setup_file, "w") as f:
                f.write(setup_content)
        package["source_dir"] = os.path.join(self.temp_dir, package["name"])
        os.makedirs(package["source_dir"])
        init_file = os.path.join(package["source_dir"], package["name"], "__init__.py")
        with open(init_file, "w", encoding="utf-8"):
            pass
        setup_content = "from setuptools import setup, find_packages\n\n" \
                        "requirements = {self.requirements!r} if {self.requirements!r} else []\n" \
                        "setup(\n" \
                        "    name='{package_name}',\n" \
                        "    version='0.1.0',\n" \
                        "    packages=find_packages(),\n" \
                        "    install_requires=requirements\n" \
                        ")\n"
        setup_file = os.path.join(package["source_dir"], "setup.py")
        with open(setup_file, "w") as f:
            f.write(setup_content)
        return package

    def install(self):
        """
        Install the dummy package and optional dependencies using pip.
        """
        for deps in self.package["deps"]:
            run(split(f"python -m pip install {deps['source_dir']} --no-input --no-dependencies"))
        run(split(f"python -m pip install {self.package['source_dir']} --no-input --no-dependencies"))

    def uninstall(self):
        """
        Uninstall the dummy package and optional dependencies using pip.
        """
        for deps in self.package["deps"]:
            run(split(f"python -m pip uninstall {deps['name']} --yes"))
        run(split(f"python -m pip uninstall {self.package['name']} --yes"))
