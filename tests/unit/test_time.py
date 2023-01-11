import os
import time
import unittest
from datetime import datetime

from assertpy import assert_that

from datamap.time import parse_timestamp


class TimeTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            os.environ['TZ'] = 'Europe/Brussels'
            time.tzset()  # will fail on Windows
        except AttributeError:
            pass

    def test_parse_timestamp_when_linux_timestamp(
        self,
    ):
        actual = parse_timestamp(1647520829437)

        assert_that(actual).is_equal_to(datetime(2022, 3, 17, 13, 40, 29, 437000))

    def test_parse_timestamp_when_none(
        self,
    ):
        assert_that(parse_timestamp(None)).is_none()

    def test_parse_timestamp_when_timestamp(
            self,
    ):
        actual = parse_timestamp(1668629719)

        assert_that(actual).is_equal_to(datetime(2022, 11, 16, 21, 15, 19))
