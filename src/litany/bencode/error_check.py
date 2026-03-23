from .util import _get_upto_first_nondigit, _get_bytestring_length

_TERMINATOR = b"e"


def _check_missing_terminator(data: bytes) -> int:
    """
    Ensures data has the 'e' terminator
    :param data: Data to check
    :type data: bytes
    :raises ValueError: Missing 'e' terminator

    :returns terminator_index:
    :rtype terminator_index: int
    """
    terminator_index: int = data.find(_TERMINATOR)
    if _TERMINATOR not in data:
        raise ValueError("Missing 'e' terminator")
    else:
        return terminator_index


def _check_has_leading_zero(data: bytes):
    """
    Ensures data does not have leading zero.
    i<base10 integer>e format expected.
    :param data: Data to check
    :type data: bytes
    :raises ValueError: Has a leading zero
    """
    n = len(data)
    # Case 1: i-0...e
    case_1 = n > 4 and data[1:3] == b"-0"

    # Case 2: i0...e;
    case_2 = n > 3 and data[1:2] == b"0"

    if case_1 or case_2:
        raise ValueError("Has a leading zero")


def _check_is_negative_zero(data: bytes):
    """
    Ensures data is not i-0e
    i<base10 integer>e format expected.
    :param data: Data to check
    :type data: bytes
    :raises ValueError: Is negative zero
    """
    if data == b"i-0e":
        raise ValueError("Is negative zero")


def _check_length_not_followed_by_colon(data: bytes):
    """
    Ensures length is followed by colon.
    <length>:<content> format expected.
    :param data: Data to check
    :type data: bytes
    :raises ValueError: Length not followed by colon
    """
    _, idx = _get_upto_first_nondigit(data, {b"-"})
    if idx == -1 or data[idx : idx + 1] != b":":
        raise ValueError("Length not followed by colon")


def _check_negative_length(data: bytes):
    """
    Ensures data does not have negative length.
    <length>:<content> format expected.
    :param data: Data to check
    :type data: bytes
    :raises ValueError: Negative length
    """
    length = _get_bytestring_length(data)
    if length < 0:
        raise ValueError("Negative length")


def _check_unexpected_eof_before_completing_string(data):
    """
    Ensures the expected length of the data is <= the length of the data
    <length>:<content> format expected
    :param data: Data to check
    :type data: bytes
    :raises ValueError: Unexpected EOF before completing string
    """
    length = _get_bytestring_length(data)
    _, first_nondigit_idx = _get_upto_first_nondigit(data, {b"-"})
    content_length = len(data[first_nondigit_idx + 1 :])
    if length > content_length:
        raise ValueError("Unexpected EOF before completing string")
