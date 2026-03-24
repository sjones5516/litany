# litany

This project is an experimental BitTorrent client. The first iteration of this
project must implement the following:

- TUI
- Parse .torrent files
- Request data from trackers
- Request data from peers
- Pause and resume downloads

In the future, seeding may be implemented.

## Instructions

### Installation

To install required dependencies, run:
`poetry install`

### Running the Software

This software is still in early development. There is not an entry-point yet.

### Running Tests

To install required testing dependencies, run:
`poetry install --with test`

To run tests, run:
`poetry run coverage run -m unittest`

To run the coverage report, run:
`poetry run coverage report -m`

## References

- [BitTorrent for Developers](https://www.bittorrent.org/beps/bep_0003.html)
- [Wikipedia - Bencode](https://en.wikipedia.org/wiki/Bencode#Types_of_errors_in_Bencode)
- [Theory.org - BitTorrent Specification](https://wiki.theory.org/BitTorrentSpecification#Identification)
