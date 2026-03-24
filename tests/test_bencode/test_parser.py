import unittest

from src.litany.bencode.parser import (
    decode,
    _parse_int,
    _parse_byte_string,
    _parse_data,
    _parse_list,
    _parse_dict,
)


class TestDecode(unittest.TestCase):
    def test_success(self):
        data = b"i0e"
        expected = 0
        actual = decode(data)
        self.assertEqual(expected, actual)

    def test_null_root_value(self):
        data = b""
        self.assertRaises(ValueError, decode, data)

    def test_non_singular_root_item(self):
        data = b"i32ei32e"
        self.assertRaises(ValueError, decode, data)


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

    def test_list(self):
        data = b"li32ei32ee"
        expected = ([32, 32], 9)
        actual = _parse_data(data)
        self.assertEqual(expected, actual)

    def test_dict(self):
        data = b"d1:ai32ee"
        expected = ({b"a": 32}, 8)
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


class TestParseList(unittest.TestCase):
    def test_empty(self):
        data = b"le"
        expected = ([], 1)
        actual = _parse_list(data)
        self.assertEqual(expected, actual)

    def test_single(self):
        data = b"li23ee"
        expected = ([23], 5)
        actual = _parse_list(data)
        self.assertEqual(expected, actual)

    def test_multiple(self):
        data = b"li23e3:abce"
        expected = ([23, b"abc"], 10)
        actual = _parse_list(data)
        self.assertEqual(expected, actual)

    def test_nested(self):
        data = b"lli23ei23eei23ee"
        expected = ([[23, 23], 23], 15)
        actual = _parse_list(data)
        self.assertEqual(expected, actual)

    def test_missing_e_terminator(self):
        data = b"li23e"
        self.assertRaises(ValueError, _parse_list, data)


class TestParseDict(unittest.TestCase):
    def test_empty(self):
        data = b"de"
        expected = ({}, 1)
        actual = _parse_dict(data)
        self.assertEqual(expected, actual)

    def test_normal(self):
        data = b"d7:meaningi42e4:wiki7:bencodee"
        expected = ({b"meaning": 42, b"wiki": b"bencode"}, 29)
        actual = _parse_dict(data)
        self.assertEqual(expected, actual)

    def test_nested(self):
        data = b"d7:meaningi42e4:wikili32eee"
        expected = ({b"meaning": 42, b"wiki": [32]}, 26)
        actual = _parse_dict(data)
        self.assertEqual(expected, actual)

    def test_missing_e_terminator(self):
        data = b"d7:meaningi42e4:wiki7:bencode"
        self.assertRaises(ValueError, _parse_dict, data)

    def test_key_is_not_a_string(self):
        data = b"di32ei32ee"
        self.assertRaises(ValueError, _parse_dict, data)

    def test_duplicate_keys(self):
        data = b"d7:meaningi42e7:meaningi24e"
        self.assertRaises(ValueError, _parse_dict, data)

    def test_keys_not_sorted(self):
        data = b"d1:bi32e1:ai32ee"
        self.assertRaises(ValueError, _parse_dict, data)

    def test_missing_value_for_key(self):
        data = b"d1:ae"
        self.assertRaises(ValueError, _parse_dict, data)
