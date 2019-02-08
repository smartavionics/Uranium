# Copyright (c) 2017 Ultimaker B.V.
# Uranium is released under the terms of the LGPLv3 or higher.

import os
import platform
from unittest import TestCase

import pytest

from UM.Resources import Resources, ResourceTypeError, UnsupportedStorageTypeError


class TestResources(TestCase):

    #
    # getConfigStorageRootPath() tests
    #
    def test_getConfigStorageRootPath_Windows(self):
        if platform.system() != "Windows":
            self.skipTest("not on Windows")

        config_root_path = Resources._getConfigStorageRootPath()
        expected_config_root_path = os.getenv("APPDATA")
        self.assertEqual(expected_config_root_path, config_root_path,
                         "expected %s, got %s" % (expected_config_root_path, config_root_path))

    def test_getConfigStorageRootPath_Linux(self):
        if platform.system() != "Linux":
            self.skipTest("not on Linux")

        # no XDG_CONFIG_HOME defined
        if "XDG_CONFIG_HOME" in os.environ:
            del os.environ["XDG_CONFIG_HOME"]
        config_root_path = Resources._getConfigStorageRootPath()
        expected_config_root_path = os.path.expanduser("~/.config")
        self.assertEqual(expected_config_root_path, config_root_path,
                         "expected %s, got %s" % (expected_config_root_path, config_root_path))

        # XDG_CONFIG_HOME defined
        os.environ["XDG_CONFIG_HOME"] = "/tmp"
        config_root_path = Resources._getConfigStorageRootPath()
        expected_config_root_path = "/tmp"
        self.assertEqual(expected_config_root_path, config_root_path,
                         "expected %s, got %s" % (expected_config_root_path, config_root_path))

    def test_getConfigStorageRootPath_Mac(self):
        if platform.system() != "Darwin":
            self.skipTest("not on mac")

        config_root_path = Resources._getConfigStorageRootPath()
        expected_config_root_path = os.path.expanduser("~/Library/Application Support")
        self.assertEqual(expected_config_root_path, config_root_path,
                         "expected %s, got %s" % (expected_config_root_path, config_root_path))

    #
    # getDataStorageRootPath() tests
    #
    def test_getDataStorageRootPath_Windows(self):
        if platform.system() != "Windows":
            self.skipTest("not on Windows")

        data_root_path = Resources._getDataStorageRootPath()
        self.assertIsNone(data_root_path, "expected None, got %s" % data_root_path)

    def test_getDataStorageRootPath_Linux(self):
        if platform.system() != "Linux":
            self.skipTest("not on Linux")

        # no XDG_CONFIG_HOME defined
        if "XDG_DATA_HOME" in os.environ:
            del os.environ["XDG_DATA_HOME"]
        data_root_path = Resources._getDataStorageRootPath()
        expected_data_root_path = os.path.expanduser("~/.local/share")
        self.assertEqual(expected_data_root_path, data_root_path,
                         "expected %s, got %s" % (expected_data_root_path, data_root_path))

        # XDG_CONFIG_HOME defined
        os.environ["XDG_DATA_HOME"] = "/tmp"
        data_root_path = Resources._getDataStorageRootPath()
        expected_data_root_path = "/tmp"
        self.assertEqual(expected_data_root_path, data_root_path,
                         "expected %s, got %s" % (expected_data_root_path, data_root_path))

    def test_getDataStorageRootPath_Mac(self):
        if platform.system() != "Darwin":
            self.skipTest("not on mac")

        data_root_path = Resources._getDataStorageRootPath()
        self.assertIsNone(data_root_path, "expected None, got %s" % data_root_path)

    #
    # getCacheStorageRootPath() tests
    #
    def test_getCacheStorageRootPath_Windows(self):
        if platform.system() != "Windows":
            self.skipTest("not on Windows")

        cache_root_path = Resources._getCacheStorageRootPath()
        expected_cache_root_path = os.getenv("LOCALAPPDATA")
        self.assertEqual(expected_cache_root_path, cache_root_path,
                         "expected %s, got %s" % (expected_cache_root_path, cache_root_path))

    def test_getCacheStorageRootPath_Linux(self):
        if platform.system() != "Linux":
            self.skipTest("not on Linux")

        cache_root_path = Resources._getCacheStorageRootPath()
        expected_cache_root_path = os.path.expanduser("~/.cache")
        self.assertEqual(expected_cache_root_path, cache_root_path,
                         "expected %s, got %s" % (expected_cache_root_path, cache_root_path))

    def test_getCacheStorageRootPath_Mac(self):
        if platform.system() != "Darwin":
            self.skipTest("not on mac")

        cache_root_path = Resources._getCacheStorageRootPath()
        self.assertIsNone("expected None, got %s" % cache_root_path)

    def test_getStoragePathForType(self):
        with pytest.raises(ResourceTypeError):
            # No types have been added, so this should break!
            Resources.getAllResourcesOfType(0)
        with pytest.raises(UnsupportedStorageTypeError):
            # We still havent added it, so it should fail (again)
            Resources.getStoragePathForType(0)

        Resources.addStorageType(0, "/test")
        assert Resources.getStoragePathForType(0) == "/test"

    def test_copyVersionFolder(self):
        import tempfile
        import os
        folder_to_copy = tempfile.mkdtemp("test_folder_origin")
        file_to_copy = tempfile.mkstemp(dir=str(folder_to_copy))

        folder_to_move_to = tempfile.mkdtemp("test_folder_destination")

        Resources.copyVersionFolder(str(folder_to_copy), str(folder_to_move_to) + "/target")
        # We put a temp file in the folder to copy, check if it arrived there.
        assert len(os.listdir(str(folder_to_move_to) + "/target")) == 1

    def test_addRemoveStorageType(self):
        Resources.addStorageType(9901, "YAY")
        Resources.addType(9902, "whoo")
        Resources.addStorageType(100, "herpderp")

        with pytest.raises(ResourceTypeError):
            # We can't add the same type again
            Resources.addStorageType(9901, "nghha")

        Resources.removeType(9001)

        with pytest.raises(ResourceTypeError):
            # We can't do that, since it's in the range of user types.
            Resources.removeType(100)

        with pytest.raises(ResourceTypeError):
            # We can't do that, since it's in the range of user types.
            Resources.addType(102, "whoo")

