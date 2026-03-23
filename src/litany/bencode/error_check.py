def _check_missing_terminator(data: bytes) -> int:
    """
    Ensures data has the 'e' terminator
    :param data: Data to check
    :type data: bytes
    :raises ValueError: Missing 'e' terminator

    :returns terminator_index:
    :rtype terminator_index: int
    """
    terminator_index: int = data.find(b"e")
    if b"e" not in data:
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