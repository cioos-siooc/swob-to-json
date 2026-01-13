#!/usr/bin/env python3
"""
Command-line interface for swob_to_json.

Usage:
    python -m swob_to_json <filename>
    python -m swob_to_json --verbose <filename>
"""

import json
import logging
import sys

import click

from swob_to_json import parseFile, __version__


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose debug output")
@click.version_option(version=__version__)
def main(filename: str, verbose: bool) -> None:
    """
    Convert a SWOB-ML XML file to JSON.

    FILENAME is the path to the SWOB-ML XML file to convert.
    Output is written to stdout.
    """
    if verbose:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(name)s - %(levelname)s - %(message)s",
            stream=sys.stderr,
        )

    swob_json = parseFile(filename)
    print(json.dumps(swob_json, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
