import unittest

from src.litany.bencode.parser import _parse_int


class TestParseInt(unittest.TestCase):
    def test_zero(self):
        data = b"i0e"
        expected = (0, 2)
        actual = _parse_int(data)
        self.assertEqual(expected, actual)

    def test_positive(self):
        data = b"i42e"
        expected = (42, 3)
        actual = _parse_int(data)
        self.assertEqual(expected, actual)

    def test_negative(self):
        data = b"i-42e"
        expected = (-42, 4)
        actual = _parse_int(data)
        self.assertEqual(expected, actual)

    def test_missing_e_terminator(self):
        data = b"i32"
        self.assertRaises(ValueError, _parse_int, data)

    def test_contains_non_digit_characters(self):
        data = b"i3a2e"
        self.assertRaises(ValueError, _parse_int, data)

    def test_has_leading_zero(self):
        data = b"i032e"
        self.assertRaises(ValueError, _parse_int, data)

    def test_is_negative_zero(self):
        data = b"i-0e"
        self.assertRaises(ValueError, _parse_int, data)
