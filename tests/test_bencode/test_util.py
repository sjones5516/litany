import unittest

from src.litany.bencode.util import (
    _get_upto_first_nondigit,
    _get_bytestring_length,
    _get_bytestring_content,
)


class TestGetUptoFirstNondigit(unittest.TestCase):
    def test_first(self):
        data = b"a123"
        expected = (b"", 0)
        actual = _get_upto_first_nondigit(data)
        self.assertEqual(expected, actual)

    def test_middle(self):
        data = b"1a23"
        expected = (b"1", 1)
        actual = _get_upto_first_nondigit(data)
        self.assertEqual(expected, actual)

    def test_last(self):
        data = b"123a"
        expected = (b"123", 3)
        actual = _get_upto_first_nondigit(data)
        self.assertEqual(expected, actual)

    def test_none(self):
        data = b"123"
        expected = (data, -1)
        actual = _get_upto_first_nondigit(data)
        self.assertEqual(expected, actual)

    def test_whitelisted(self):
        data = b"-023"
        whitelist = {b"-"}
        expected = (data, -1)
        actual = _get_upto_first_nondigit(data, whitelist)
        self.assertEqual(expected, actual)


class TestGetBytestringLength(unittest.TestCase):
    def test_positive(self):
        data = b"3:abc"
        expected = 3
        actual = _get_bytestring_length(data)
        self.assertEqual(expected, actual)

    def test_negative(self):
        data = b"-3:abc"
        expected = -3
        actual = _get_bytestring_length(data)
        self.assertEqual(expected, actual)


class TestGetBytestringContent(unittest.TestCase):
    def test_exact(self):
        data = b"2:aa"
        expected = b"aa"
        actual = _get_bytestring_content(data)
        self.assertEqual(expected, actual)

    def test_excess(self):
        data = b"1:aa"
        expected = b"a"
        actual = _get_bytestring_content(data)
        self.assertEqual(expected, actual)
