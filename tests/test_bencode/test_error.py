import unittest

from src.litany.bencode.error_check import (
    _check_has_leading_zero,
    _check_length_not_followed_by_colon,
    _check_unexpected_eof_before_completing_string,
)


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


class TestLengthNotFollowedByColon(unittest.TestCase):
    def test_succeeds(self):
        data = b"1:e"
        _check_length_not_followed_by_colon(data)

    def test_nocolon(self):
        data = b"1e"
        self.assertRaises(ValueError, _check_length_not_followed_by_colon, data)

    def test_colon_after_char(self):
        data = b"1a:e"
        self.assertRaises(ValueError, _check_length_not_followed_by_colon, data)


class TestUnexpectedEOFBeforeCompletingString(unittest.TestCase):
    def test_succeeds(self):
        data = b"1:a"
        _check_unexpected_eof_before_completing_string(data)

    def test_zero_length(self):
        data = b"0:"
        _check_unexpected_eof_before_completing_string(data)

    def test_too_long(self):
        data = b"3:ab"
        self.assertRaises(
            ValueError, _check_unexpected_eof_before_completing_string, data
        )
