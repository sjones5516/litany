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
    _check_null_root_value,
    _check_non_singular_root_item,
)

from .util import (
    _get_bytestring_content,
    _get_bytestring_expected_total_data_length,
    _get_datatype,
    CHUNK_TYPES,
)


def decode(data: bytes) -> CHUNK_TYPES:
    """
    Parses bytes of some bencoded format
    :param data: Data to parse
    :type data: bytes

    :raises ValueError: Non-singular root item
    :raises ValueError: Null root value
    :raises ValueError: Missing 'e' terminator
    :raises ValueError: Has a leading zero
    :raises ValueError: Is negative zero
    :raises ValueError: Contains non-digit characters
    :raises ValueError: Negative length
    :raises ValueError: Length not followed by colon
    :raises ValueError: Unexpected EOF before completing string
    :raises ValueError: Key is not a string
    :raises ValueError: Duplicate keys
    :raises ValueError: Keys not sorted
    :raises ValueError: Missing value for a key

    :returns parsed data:
    :rtype CHUNK_TYPES:
    """
    _check_null_root_value(data)
    parsed_data, end = _parse_data(data)
    _check_non_singular_root_item(data, end)
    return parsed_data


def _parse_data(data: bytes) -> tuple[CHUNK_TYPES, int]:
    """
    Parses bytes of some bencoded format
    :param data: Data to parse
    :type data: bytes

    :raises ValueError: Missing 'e' terminator
    :raises ValueError: Has a leading zero
    :raises ValueError: Is negative zero
    :raises ValueError: Contains non-digit characters
    :raises ValueError: Negative length
    :raises ValueError: Length not followed by colon
    :raises ValueError: Unexpected EOF before completing string
    :raises NotImplementedError: Tries to parse list or dict

    :returns (parsed integer, end index):
    :rtype tuple[int, int]:
    """
    datatype = _get_datatype(data)
    if datatype is int:
        return _parse_int(data)
    elif datatype is bytes:
        return _parse_byte_string(data)
    elif datatype is list:
        return _parse_list(data)
    else:
        return _parse_dict(data)


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

    :raises ValueError: Negative length
    :raises ValueError: Length not followed by colon
    :raises ValueError: Unexpected EOF before completing string

    :returns (parsed bytes, end index):
    :rtype tuple[bytes, int]:
    """
    assert data[0:1] in b"123456790-"
    _check_length_not_followed_by_colon(data)
    _check_negative_length(data)
    _check_unexpected_eof_before_completing_string(data)
    content = _get_bytestring_content(data)
    end = _get_bytestring_expected_total_data_length(data) - 1
    return content, end


def _parse_list(data: bytes) -> tuple[list, int]:
    """
    Parses bytes formatted as l<contents>e
    :param data: Data to parse
    :type data: bytes

    :raises ValueError: Missing 'e' terminator

    :returns (parsed list, end index):
    :rtype tuple[list, int]:
    """
    assert data[0:1] == b"l"
    absolute_cursor = 1
    search_space = data[1:]
    return_data = list()
    while len(search_space) > 0:
        if search_space[0:1] == b"e":
            break

        content, end = _parse_data(search_space)
        return_data.append(content)
        absolute_cursor += end + 1
        search_space = search_space[end + 1 :]

    if data[absolute_cursor : absolute_cursor + 1] != b"e":
        raise ValueError("Missing 'e' terminator")

    return (return_data, absolute_cursor)


def _parse_dict(data: bytes) -> tuple[dict, int]:
    """
    Parses bytes formatted as d<contents>e
    :param data: Data to parse
    :type data: bytes

    :raises ValueError: Missing 'e' terminator
    :raises ValueError: Key is not a string
    :raises ValueError: Duplicate keys
    :raises ValueError: Keys not sorted
    :raises ValueError: Missing value for a key

    :returns (parsed dict, end index):
    :rtype tuple[dict, int]:
    """
    assert data[0:1] == b"d"
    absolute_cursor = 1
    search_space = data[1:]
    prev_key = None
    return_data = dict()
    while len(search_space) > 0:
        if search_space[0:1] == b"e":
            break

        key_content, end = _parse_data(search_space)
        absolute_cursor += end + 1

        if type(key_content) is not bytes:
            raise ValueError("Key is not string")

        if key_content in return_data:
            raise ValueError("Duplicate keys")

        if prev_key is not None and prev_key > key_content:
            raise ValueError("Keys not sorted")

        search_space = search_space[end + 1 :]
        prev_key = key_content

        if search_space[0:1] == b"e":
            raise ValueError("Missing value for a key")

        value_content, end = _parse_data(search_space)
        return_data[key_content] = value_content
        absolute_cursor += end + 1
        search_space = search_space[end + 1 :]

    if data[absolute_cursor : absolute_cursor + 1] != b"e":
        raise ValueError("Missing 'e' terminator")

    return (return_data, absolute_cursor)
