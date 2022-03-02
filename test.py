#!/usr/bin/python3
# Copyright (C) 2022 Gaurav Kedia. All rights reserved.
""" Unit Test Temperature API """
import unittest
from main import get_temp_url, get_temp


class TestRestMethods(unittest.TestCase):
    """
    Class to unittest methods from main module.

    """
    new_latitude = '0'
    new_longitude = '0'

    def test_get_temp_url(self):
        """
        Code below will unittest get_temp_url method.

        """
        expected_url = get_temp_url(self.new_latitude, self.new_longitude)
        fake_url = "value"
        self.assertFalse(expected_url == fake_url)

    def test_get_temp(self):
        """
        Code below will unittest get_temp method.

        """
        result = get_temp(self.new_latitude, self.new_longitude)
        self.assertEqual(result, True)


if __name__ == '__main__':
    unittest.main()
