#!/usr/bin/env python3
"""
SWOB-ML to JSON converter.

This module provides functions to parse SWOB-ML (Surface Weather and Marine
Observation Markup Language) XML files from Environment and Climate Change
Canada (ECCC) and convert them to a flat JSON structure suitable for
tabular data processing.

Example usage:
    from swob_to_json import parseFile, parseText

    # Parse from file
    result = parseFile("path/to/swob.xml")

    # Parse from string
    result = parseText(xml_string)
"""

import logging
from typing import Any, Dict, Optional, Union

import xmltodict

from swob_to_json.constants import (
    CCG_WIND_DIRECTION_MAP,
    INTEGER_KEY_SUFFIXES,
    MISSING_VALUE,
    NUMERIC_METADATA_FIELDS,
)
from swob_to_json.flatten_json import flatten_json

logger = logging.getLogger(__name__)


def replace_values(
    input_dict: Dict[str, Any],
    from_value: Any,
    to_value: Any
) -> Dict[str, Any]:
    """
    Replace all occurrences of a value in a dictionary's values.

    Performs in-place replacement at the top level of the dictionary only
    (non-recursive). Returns the modified dictionary for convenience.

    Args:
        input_dict: Dictionary to modify.
        from_value: Value to search for and replace.
        to_value: Value to replace with.

    Returns:
        The modified input dictionary (same object, mutated).

    Example:
        >>> d = {"a": "MSNG", "b": 1.0, "c": "MSNG"}
        >>> replace_values(d, "MSNG", None)
        {"a": None, "b": 1.0, "c": None}
    """
    for key, val in input_dict.items():
        if val == from_value:
            input_dict[key] = to_value
    return input_dict


def parseFile(xml_file_path: str) -> Dict[str, Any]:
    """
    Parse a SWOB-ML XML file and convert to JSON-compatible dictionary.

    Args:
        xml_file_path: Path to the SWOB-ML XML file.

    Returns:
        Dictionary containing parsed weather observation data with keys:
        - sampling_time: ISO timestamp of the observation
        - result_time: ISO timestamp when result was recorded
        - metadata: Station metadata (location, IDs, etc.)
        - results: Observation values (temperature, wind, pressure, etc.)

    Raises:
        FileNotFoundError: If the specified file does not exist.
        xmltodict.expat.ExpatError: If the XML is malformed.
    """
    logger.debug("Parsing file: %s", xml_file_path)
    with open(xml_file_path, "r", encoding="utf-8") as content_file:
        xml_string = content_file.read()
    return parseText(xml_string)


def parse_ccg_wind_direction(value: Union[int, str]) -> Optional[float]:
    """
    Convert CCG/ECCC wind direction code to compass degrees.

    The Canadian Coast Guard (CCG) and Environment and Climate Change Canada
    (ECCC) use integer codes 0-21 to represent wind directions. This function
    converts those codes to compass degrees (0-360).

    Args:
        value: Wind direction code (0-21) as integer or string.

    Returns:
        Compass degrees as float (0.0-337.5), or None for codes that represent
        non-directional conditions (calm, variable, not reported, etc.).

    Example:
        >>> parse_ccg_wind_direction(8)  # North
        0.0
        >>> parse_ccg_wind_direction(4)  # South
        180.0
        >>> parse_ccg_wind_direction(0)  # Calm
        None
    """
    return CCG_WIND_DIRECTION_MAP.get(str(value), None)


def is_integer_key(key: str) -> bool:
    """
    Determine if a field key should be parsed as an integer.

    Fields ending with certain suffixes (code, summary, flag) are stored
    as integers rather than floats in SWOB data.

    Args:
        key: The field name to check.

    Returns:
        True if the key ends with an integer suffix, False otherwise.

    Example:
        >>> is_integer_key("wnd_dir_code")
        True
        >>> is_integer_key("air_temp")
        False
    """
    return key.endswith(INTEGER_KEY_SUFFIXES)


def parseText(xml_string: str) -> Dict[str, Any]:
    """
    Parse SWOB-ML XML string and convert to JSON-compatible dictionary.

    This is the main parsing function that:
    1. Parses XML using xmltodict
    2. Flattens the nested XML structure
    3. Replaces missing value markers with None
    4. Converts numeric fields to appropriate types (int or float)
    5. Converts wind direction codes to compass degrees

    Args:
        xml_string: SWOB-ML XML content as a string.

    Returns:
        Dictionary containing parsed weather observation data with keys:
        - sampling_time: ISO timestamp of the observation (or None if missing)
        - result_time: ISO timestamp when result was recorded (or None if missing)
        - metadata: Station metadata (location, IDs, etc.)
        - results: Observation values (temperature, wind, pressure, etc.)

    Raises:
        xmltodict.expat.ExpatError: If the XML is malformed.
    """
    logger.debug("Parsing XML string of length %d", len(xml_string))

    data_dict = xmltodict.parse(xml_string)

    # Parse out a flat dictionary of the data/metadata fields
    record = flatten_json(data_dict)

    # Replace fill values with None before numeric conversion
    # to avoid conversion errors on "MSNG" strings
    replace_values(record["results"], MISSING_VALUE, None)

    # Convert results to numeric types
    for key, value in record["results"].items():
        if value is None:
            continue
        try:
            # Code, flag, and summary fields are integers
            if is_integer_key(key):
                record["results"][key] = int(value)
            else:
                record["results"][key] = float(value)
        except (ValueError, TypeError) as e:
            logger.debug("Could not convert result '%s' value '%s': %s", key, value, e)

    # Convert a few metadata fields to numeric
    for key, value in record["metadata"].items():
        if value is None:
            continue
        try:
            if key in NUMERIC_METADATA_FIELDS:
                record["metadata"][key] = float(value)
        except (ValueError, TypeError) as e:
            logger.debug("Could not convert metadata '%s' value '%s': %s", key, value, e)

    replace_values(record["metadata"], MISSING_VALUE, None)

    # Check for CCG wind direction code and convert to degrees
    if "wnd_dir_code" in record["results"]:
        try:
            code_value = record["results"]["wnd_dir_code"]
            record["results"]["wnd_dir"] = parse_ccg_wind_direction(int(code_value))
            logger.debug("Converted wnd_dir_code %s to wnd_dir %s",
                        code_value, record["results"]["wnd_dir"])
        except (ValueError, TypeError) as e:
            logger.warning("Could not convert wnd_dir_code: %s", e)

    return record
