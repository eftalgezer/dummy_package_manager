"""
This module provides test scenarios using the DummyPackageTester class to test the DummyPackage class.
"""

from .testers import DummyPackageTester, __exit___tester


def test_DummyPackage():
    """
    Test the functionality of the DummyPackage class using various scenarios.
    """
    test_tester = None
    with DummyPackageTester("package1", requirements=["package2"]) as tester:
        test_tester = tester
        assert tester.package
        assert tester.package["name"] == "package1"
        assert tester.package["deps"][0]["name"] == "package2"
        assert tester.install_tester()
        assert tester.uninstall_tester()
        assert tester.install_tester()
    assert __exit___tester(test_tester)
    test_tester = None
    with DummyPackageTester("package1") as tester:
        test_tester = tester
        assert tester.package
        assert tester.package["name"] == "package1"
        assert tester.package["deps"] == []
        assert tester.install_tester()
        assert tester.uninstall_tester()
        assert tester.install_tester()
    assert __exit___tester(test_tester)
