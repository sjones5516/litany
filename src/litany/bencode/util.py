def _get_upto_first_nondigit(
    data: bytes, whitelist: set[bytes] = {}
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
