"""
This module provides the Metainfo class for parsing a .torrent file.
"""

from typing import Optional, Union


class Metainfo:
    """
    For parsing a .torrent file and mapping to the specification
    :ivar info: A dictionary describes the file(s) of a torrent
    :ivar announce: The announce URL of the tracker
    :ivar creation_date: The creation time of the torrent, in standard UNIX epoch format
    :ivar comment: free-form textual comments of the author
    :ivar created by: (optional) name and version of the program used to create the .torrent
    :ivar encoding: (optional) the string encoding format used to generate the pieces part of the info dicionary in the metafile
    """

    info: Union[SingleFileInfoDictionary, MultipleFileInfoDictionary]
    announce: str
    creation_date: Optional[str]
    comment: Optional[str]
    created_by: Optional[str]
    encoding: Optional[str]


class InfoDictionary:
    """
    Parent class for metainfo info dictionary
    :ivar piece_length: number of bytes in each piece
    :ivar pieces: string consisting of the concatenation of all 20-byte SHA1 hash values, one per piece
    :ivar private: (optional) if set to "1" the client MUST publish its presence to get other peers ONLY via the trackers explicitly mentioned in the metainfo file
    """

    piece_length: int
    pieces: bytes
    private: Optional[int]


class SingleFileInfoDictionary(InfoDictionary):
    """
    Info dictionary for a metainfo file in single-file mode
    :ivar name: the filename
    :ivar length: the length of the file in bytes
    :ivar md5sum: (optional) a 32-character hex string corresponding to the md5sum of the file
    """

    name: str
    length: int
    md5sum: Optional[bytes]


class MultipleFileInfoDictionary(InfoDictionary):
    """
    Info dictionary for a metainfo file in multiple-file mode
    :ivar name: The name of the directory to store all the files
    :ivar files: A list of dictionaries, one for each file. Each dictionary contains the following keys:
    length: the length of the file in bytes (integer)
    md5sum: (optional) a 32-character hex string corresponding to the md5sum of the file
    path: a list containing one or more string elements that together represent the path and filename. Each element corresponds to either a directory name or (in the case of the final element) the filename.
    """

    name: str
    files: dict
