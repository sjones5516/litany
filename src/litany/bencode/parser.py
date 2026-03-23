"""
This module provides utility functions for parsing bencoded data.
For reference, see https://en.wikipedia.org/wiki/Bencode
"""

from .error_check import (
    _check_missing_terminator,
    _check_has_leading_zero,
    _check_is_negative_zero,
    _check_length_not_followed_by_colon,
    _check_negative_length,
    _check_unexpected_eof_before_completing_string,
)

from .util import _get_bytestring_content, _get_bytestring_expected_total_data_length


def _parse_int(data: bytes) -> tuple[int, int]:
    """
    Parses bytes formatted as i<base10 integer>e
    :param data: Data to parse
    :type data: bytes

    :raises ValueError: Missing 'e' terminator
    :raises ValueError: Has a leading zero
    :raises ValueError: Is negative zero
    :raises ValueError: Contains non-digit characters

    :returns (parsed integer, end index):
    :rtype tuple[int, int]:
    """
    assert data[0:1] == b"i"
    terminator_index = _check_missing_terminator(data)
    _check_has_leading_zero(data)
    _check_is_negative_zero(data)

    # removes the prefix and terminator
    int_bytes = data[1:terminator_index]

    # converting the bytes to an integer implicitly checks for non-digit characters, so an explicit check method is not used
    try:
        return int(int_bytes), terminator_index
    except ValueError:
        raise ValueError("Contains non-digit characters")


def _parse_byte_string(data: bytes) -> tuple[bytes, int]:
    """
    Parses bytes formatted as <length>:<contents>
    :param data: Data to parse
    :type data: bytes

    :returns (parsed bytes, end index):
    :rtype tuple[int, int]:
    """
    _check_length_not_followed_by_colon(data)
    _check_negative_length(data)
    _check_unexpected_eof_before_completing_string(data)
    content = _get_bytestring_content(data)
    end = _get_bytestring_expected_total_data_length(data) - 1
    return content, end

