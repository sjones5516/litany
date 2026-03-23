_BYTESTRING_WHITELIST = {b"-"}

def _get_datatype(data: bytes) -> type:
    """
    Find the type of data based on the prefix.
    :param data: Data to check
    :type data: bytes
    :raises ValueError: Invalid type encountered
    :returns Type of data:
    :rtype: CHUNK_TYPES
    """
    assert len(data) >= 1
    prefix = data[0:1]
    if prefix == b"i":
        return int
    elif prefix == b"l":
        return list
    elif prefix == b"d":
        return dict
    elif prefix in b"123456790-":
        return bytes
    else:
        raise ValueError("Invalid type encountered")


def _get_upto_first_nondigit(
    data: bytes, whitelist: set[bytes] = set()
) -> tuple[bytes, int]:
    """
    Gets up to the first nondigit character in data.
    If no nondigit character is found, returns (data, -1)
    :param data: Data to parse
    :type data: bytes
    :param whitelist: Whitelisted nondigit characters; These are ignored
    :type whitelist: set[bytes]

    :returns (data up to first non digit, index of first nondigit):
    :rtype tuple[bytes, int]
    """

    for i in range(0, len(data)):
        char = data[i : i + 1]
        if not char.isdigit() and char not in whitelist:
            return (data[0:i], i)

    return (data, -1)


def _get_bytestring_length(data: bytes) -> int:
    """
    Gets the length of a bytestring as denoted by the prefix.
     <length>:<content> format expected.
     :param data: Data to parse
     :type data: bytes

     :returns length:
     :rtype int
    """
    colon_index = data.find(b":")
    data_length_bytes = data[0:colon_index]

    return int(data_length_bytes)


def _get_bytestring_content(data: bytes) -> bytes:
    """
    Gets the content of a bytestring.
     <length>:<content> format expected.
     :param data: Data to parse
     :type data: bytes

     :returns content:
     :rtype bytes
    """
    colon_index = data.find(b":")
    length = _get_bytestring_length(data)
    return data[colon_index + 1 : colon_index + length + 1]


def _get_bytestring_expected_total_data_length(data: bytes) -> int:
    """
    Gets the expected total length of a bytestring.
     <length>:<content> format expected.
     :param data: Data to parse
     :type data: bytes

     :returns length:
     :rtype bytes
    """
    length_bytes, _ = _get_upto_first_nondigit(data, _BYTESTRING_WHITELIST)
    length = _get_bytestring_length(data)
    return len(length_bytes) + length + 1
