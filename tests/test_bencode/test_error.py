import unittest

from src.litany.bencode.error_check import (
    _check_missing_terminator,
    _check_has_leading_zero,
    _check_is_negative_zero,
)


class TestCheckMissingTerminator(unittest.TestCase):
    def test_succeeds(self):
        data = b"i23e"
        _check_missing_terminator(data)

    def test_fails(self):
        data = b"i23"
        self.assertRaises(ValueError, _check_missing_terminator, data)


class TestCheckHasLeadingZero(unittest.TestCase):
    def test_succeeds(self):
        data = b"i2e"
        _check_has_leading_zero(data)

    def test_fails_case_1(self):
        data = b"i-02e"
        self.assertRaises(ValueError, _check_has_leading_zero, data)

    def test_fails_case_2(self):
        data = b"i02e"
        self.assertRaises(ValueError, _check_has_leading_zero, data)

class TestCheckIsNegativeZero(unittest.TestCase):
    def test_succeeds(self):
        data = b"i0e"
        _check_is_negative_zero(data)
    
    def test_fails(self):
        data = b"i-0e"
        self.assertRaises(ValueError, _check_is_negative_zero, data)