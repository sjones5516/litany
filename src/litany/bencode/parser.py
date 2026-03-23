"""
This module provides utility functions for parsing bencoded data.
For reference, see https://en.wikipedia.org/wiki/Bencode
"""

from .error_check import (
    _check_missing_terminator,
    _check_has_leading_zero,
    _check_is_negative_zero,
)


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
