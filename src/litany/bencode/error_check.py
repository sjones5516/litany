def _check_missing_terminator(data: bytes):
    """
    Ensures data has the 'e' terminator
    :param data: Data to check
    :type data: bytes
    :raises ValueError: Missing 'e' terminator
    """
    if b"e" not in data:
        raise ValueError("Missing 'e' terminator")
