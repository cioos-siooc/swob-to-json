#!/usr/bin/env python3
"""
Flatten nested SWOB-ML XML structure into a simple dictionary.

This module handles the extraction of data from the deeply nested XML
structure produced by xmltodict when parsing SWOB-ML files.
"""

import logging
from typing import Any, Dict, Optional

from swob_to_json.ungroup_elements import ungroup_elements

logger = logging.getLogger(__name__)


def flatten_json(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Flatten the nested dictionary structure from xmltodict into tabular form.

    Extracts observation results, station metadata, and timestamps from the
    deeply nested SWOB-ML XML structure and returns them in a flat dictionary
    suitable for tabular data processing.

    Args:
        data: Nested dictionary produced by xmltodict.parse() on SWOB-ML XML.

    Returns:
        Dictionary with the following structure:
        {
            "sampling_time": str or None,  # ISO timestamp of observation
            "result_time": str or None,    # ISO timestamp of result recording
            "metadata": dict,              # Station metadata (location, IDs, etc.)
            "results": dict,               # Observation values
        }

    Note:
        If any expected XML paths are missing, the corresponding values will
        be empty dicts or None rather than raising an exception. This allows
        partial parsing of malformed or incomplete SWOB files.
    """
    # 'results' and 'metadata' stored at different paths in the XML.
    # results & metadata are dictionaries

    # Handle case where result elements might be missing or empty
    try:
        result_elements = data["om:ObservationCollection"]["om:member"]["om:Observation"]["om:result"]["elements"].get("element")
        results = ungroup_elements(result_elements)
    except (KeyError, TypeError) as e:
        logger.debug("Could not extract result elements: %s", e)
        results = {}

    # Handle case where metadata elements might be missing or empty
    try:
        metadata_elements = data["om:ObservationCollection"]["om:member"]["om:Observation"]["om:metadata"]["set"]["identification-elements"].get("element")
        metadata = ungroup_elements(metadata_elements)
    except (KeyError, TypeError) as e:
        logger.debug("Could not extract metadata elements: %s", e)
        metadata = {}

    # Extract timestamps with error handling
    sampling_time = _extract_timestamp(data, "om:samplingTime")
    result_time = _extract_timestamp(data, "om:resultTime")

    # Combine all of these
    record = {
        "sampling_time": sampling_time,
        "result_time": result_time,
        "metadata": metadata,
        "results": results,
    }

    return record


def _extract_timestamp(data: Dict[str, Any], time_key: str) -> Optional[str]:
    """
    Extract a timestamp from the SWOB-ML XML structure.

    Args:
        data: Nested dictionary from xmltodict.parse().
        time_key: The key for the time element (e.g., "om:samplingTime").

    Returns:
        ISO timestamp string, or None if the path doesn't exist.
    """
    try:
        return data["om:ObservationCollection"]["om:member"]["om:Observation"][
            time_key
        ]["gml:TimeInstant"]["gml:timePosition"]
    except (KeyError, TypeError) as e:
        logger.debug("Could not extract %s: %s", time_key, e)
        return None
