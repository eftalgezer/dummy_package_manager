"""
This module provides test scenarios using the DummyPackageTester class to test the DummyPackage class.
"""

import shutil
from unittest.mock import patch
from .testers import DummyPackageTester


def test_DummyPackage():
    """
    Test the functionality of the DummyPackage class using various scenarios.
    """
    with patch.object(DummyPackageTester, "__exit__", return_value=None):
        with DummyPackageTester("package1", requirements=["package2"]) as tester:
            assert tester.package
            assert tester.package["name"] == "package1"
            assert tester.package["deps"][0]["name"] == "package2"
            assert tester.install_tester()
            assert tester.package["is_installed"]
            assert tester.uninstall_tester()
            assert not tester.package["is_installed"]
            assert tester.install_tester()
            assert tester.package["is_installed"]
            assert tester.uninstall_tester()
            assert not tester.package["is_installed"]
            shutil.rmtree(tester.temp_dir)
    with patch.object(DummyPackageTester, "__exit__", return_value=None):
        with DummyPackageTester("package1") as tester:
            assert tester.package
            assert tester.package["name"] == "package1"
            assert tester.package["deps"] == []
            assert tester.install_tester()
            assert tester.package["is_installed"]
            assert tester.uninstall_tester()
            assert not tester.package["is_installed"]
            assert tester.install_tester()
            assert tester.package["is_installed"]
            assert tester.uninstall_tester()
            assert not tester.package["is_installed"]
            shutil.rmtree(tester.temp_dir)
