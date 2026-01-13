#!/usr/bin/env python3
"""
Convert SWOB-ML element structures to flat key-value pairs.

This module handles the conversion of the nested <element> and <qualifier>
XML structures in SWOB-ML into simple dictionaries.
"""

import logging
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)


def ungroup_elements(elements: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]) -> Dict[str, str]:
    """
    Convert SWOB-ML element XML structure to flat key-value pairs.

    Takes the JSON representation of SWOB-ML <element> tags (as produced by
    xmltodict) and converts them to a simple dictionary mapping element names
    to their values. Qualifier sub-elements are included with compound keys.

    Example XML structure:
        <elements>
            <element name="wind_speed" value="5.0">
                <qualifier name="time_duration" value="2" />
            </element>
        </elements>

    Becomes:
        {"wind_speed": "5.0", "wind_speed_time_duration": "2"}

    Args:
        elements: Either a single element dict, a list of element dicts,
                  or None. The xmltodict library returns a dict for single
                  elements and a list for multiple elements.

    Returns:
        Dictionary mapping element names (and qualifier compound names) to
        their string values. Returns empty dict if elements is None.

    Note:
        All values are returned as strings. Numeric conversion happens
        in the main parseText() function.
    """
    # Handle case where elements is None or empty
    if elements is None:
        return {}

    # xmltodict returns a dict for single element, list for multiple
    # Normalize to always work with a list
    if not isinstance(elements, list):
        elements = [elements]

    results: Dict[str, str] = {}
    for element in elements:
        element_name = element["@name"]
        results[element_name] = element["@value"]

        if "qualifier" in element:
            # Normalize qualifiers to list (xmltodict inconsistency)
            qualifiers = element["qualifier"]
            if not isinstance(qualifiers, list):
                qualifiers = [qualifiers]

            # There can be multiple qualifiers per element
            for qualifier in qualifiers:
                compound_key = f"{element_name}_{qualifier['@name']}"
                results[compound_key] = qualifier["@value"]

    return results
