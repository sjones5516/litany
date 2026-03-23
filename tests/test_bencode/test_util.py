import unittest

from src.litany.bencode.util import _get_upto_first_nondigit


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
