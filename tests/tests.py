"""
This module provides test scenarios using the DummyPackageTester class to test the DummyPackage class.
"""

import shutil
from subprocess import Popen
from shlex import split
from unittest import TestCase
from .testers import DummyPackageTester, __exit___tester


def test_DummyPackage():
    """
    Test the functionality of the DummyPackage class using various scenarios.
    """
    tester = DummyPackageTester("package1", requirements=["package2"])
    with tester:
        assert tester.package
        assert tester.package["name"] == "package1"
        assert tester.package["deps"][0]["name"] == "package2"
        tester.install_tester()
        assert tester.package["is_installed"]
        tester.uninstall_tester()
        assert not tester.package["is_installed"]
        tester.install_tester()
        assert tester.package["is_installed"]
    __exit___tester(tester)
    tester = DummyPackageTester("package1")
    with tester:
        assert tester.package
        assert tester.package["name"] == "package1"
        assert tester.package["deps"] == []
        tester.install_tester()
        assert tester.package["is_installed"]
        tester.uninstall_tester()
        assert not tester.package["is_installed"]
        tester.install_tester()
        assert tester.package["is_installed"]
    __exit___tester(tester)
    tester = DummyPackageTester("package1", requirements=["package2"])
    with tester:
        assert tester.package
        assert tester.package["name"] == "package1"
        assert tester.package["deps"][0]["name"] == "package2"
        shutil.rmtree(tester.package["deps"][0]["source_dir"])
        with TestCase().assertRaises(ImportError):
            tester.install_tester()
    tester = DummyPackageTester("package1", requirements=["package2"])
    with tester:
        assert tester.package
        assert tester.package["name"] == "package1"
        assert tester.package["deps"][0]["name"] == "package2"
        shutil.rmtree(tester.package["source_dir"])
        with TestCase().assertRaises(ImportError):
            tester.install_tester()
    tester = DummyPackageTester("package1", requirements=["package2"])
    with TestCase().assertRaises(ImportError):
        with tester:
            assert tester.package
            assert tester.package["name"] == "package1"
            assert tester.package["deps"][0]["name"] == "package2"
            tester.install_tester()
            with Popen(split(f"python -m pip uninstall {tester.package['deps'][0]['name']} --yes")):
                with TestCase().assertRaises(ImportError, FileNotFoundError):
                    tester.uninstall_tester()
    tester = DummyPackageTester("package1", requirements=["package2"])
    with TestCase().assertRaises(ImportError):
        with tester:
            assert tester.package
            assert tester.package["name"] == "package1"
            assert tester.package["deps"][0]["name"] == "package2"
            tester.install_tester()
            with Popen(split(f"python -m pip uninstall {tester.package['name']} --yes")):
                with TestCase().assertRaises(ImportError):
                    tester.uninstall_tester()
