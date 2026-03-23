import unittest

from src.litany.bencode.parser import _parse_int, _parse_byte_string, _parse_data


class TestParseData(unittest.TestCase):
    def test_int(self):
        data = b"i0e"
        expected = (0, 2)
        actual = _parse_data(data)
        self.assertEqual(expected, actual)

    def test_bytestring(self):
        data = b"3:abc"
        expected = (b"abc", 4)
        actual = _parse_data(data)
        self.assertEqual(expected, actual)


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


class TestParseByteString(unittest.TestCase):
    def test_empty(self):
        data = b"0:"
        expected = (b"", 1)
        actual = _parse_byte_string(data)
        self.assertEqual(expected, actual)

    def test_normal(self):
        data = b"3:abc"
        expected = (b"abc", 4)
        actual = _parse_byte_string(data)
        self.assertEqual(expected, actual)

    def test_excess(self):
        data = b"3:abcde"
        expected = (b"abc", 4)
        actual = _parse_byte_string(data)
        self.assertEqual(expected, actual)

    def test_negative_length(self):
        data = b"-3:abc"
        self.assertRaises(ValueError, _parse_byte_string, data)

    def test_length_not_followed_by_colon(self):
        data = b"-3a:abc"
        self.assertRaises(ValueError, _parse_byte_string, data)

    def test_length_not_followed_by_colon_no_colon(self):
        data = b"-3aabc"
        self.assertRaises(ValueError, _parse_byte_string, data)

    def test_unexpected_eof_before_completing_string(self):
        data = b"3:ab"
        self.assertRaises(ValueError, _parse_byte_string, data)
