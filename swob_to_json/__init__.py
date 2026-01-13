"""
SWOB-to-JSON: Convert SWOB-ML XML to JSON.

This package provides utilities to parse SWOB-ML (Surface Weather and Marine
Observation Markup Language) XML files from Environment and Climate Change
Canada (ECCC) and convert them to a flat JSON structure.

Example usage:
    from swob_to_json import parseFile, parseText

    # Parse from file
    result = parseFile("path/to/swob.xml")

    # Parse from string
    result = parseText(xml_string)

The result dictionary contains:
    - sampling_time: ISO timestamp of the observation
    - result_time: ISO timestamp when result was recorded
    - metadata: Station metadata (location, IDs, etc.)
    - results: Observation values (temperature, wind, pressure, etc.)
"""

from swob_to_json.swob_to_json import parseFile, parseText, parse_ccg_wind_direction

__version__ = "1.1.0"
__all__ = ["parseFile", "parseText", "parse_ccg_wind_direction", "__version__"]
