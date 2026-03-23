import unittest

from src.litany.bencode.error_check import _check_missing_terminator


class TestCheckMissingTerminator(unittest.TestCase):
    def test_succeeds(self):
        data = b"i23e"
        _check_missing_terminator(data)

    def test_fails(self):
        data = b"i23"
        self.assertRaises(ValueError, _check_missing_terminator, data)
