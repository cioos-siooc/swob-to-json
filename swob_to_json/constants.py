#!/usr/bin/env python3
"""
Constants used throughout the swob_to_json package.

This module contains magic values, field mappings, and configuration constants
extracted from throughout the codebase for maintainability.
"""

from typing import Dict, Optional, Set

# Fill value used in SWOB-ML to indicate missing data
MISSING_VALUE: str = "MSNG"

# Metadata fields that should be converted to float
NUMERIC_METADATA_FIELDS: Set[str] = {"lat", "long", "stn_elev"}

# Key suffixes that indicate integer values (codes, flags, summaries)
INTEGER_KEY_SUFFIXES: tuple[str, ...] = ("_code", "_summary", "_flag")

# CCG (Canadian Coast Guard) wind direction code to compass degrees mapping
# Based on ECCC (Environment and Climate Change Canada) coding standards
# Reference: https://dd.weather.gc.ca/observations/doc/
CCG_WIND_DIRECTION_MAP: Dict[str, Optional[float]] = {
    "0": None,      # Calm
    "1": 45.0,      # Northeast (NE)
    "2": 90.0,      # East (E)
    "3": 135.0,     # Southeast (SE)
    "4": 180.0,     # South (S)
    "5": 225.0,     # Southwest (SW)
    "6": 270.0,     # West (W)
    "7": 315.0,     # Northwest (NW)
    "8": 0.0,       # North (N)
    "9": None,      # Variable/All directions/confused/unknown
    "10": None,     # Not reported
    "11": None,     # Ship in shore or flaw lead
    "12": None,     # Not determined (ship in ice)
    "13": None,     # Unable to report due to darkness, etc.
    "14": 22.5,     # North-northeast (NNE)
    "15": 67.5,     # East-northeast (ENE)
    "16": 112.5,    # East-southeast (ESE)
    "17": 157.5,    # South-southeast (SSE)
    "18": 202.5,    # South-southwest (SSW)
    "19": 247.5,    # West-southwest (WSW)
    "20": 292.5,    # West-northwest (WNW)
    "21": 337.5,    # North-northwest (NNW)
}

# XML namespace paths used in SWOB-ML documents
# These correspond to the om: (Observations & Measurements) and gml: (Geography Markup Language) namespaces
XML_PATHS = {
    "observation": "om:ObservationCollection.om:member.om:Observation",
    "results": "om:result.elements.element",
    "metadata": "om:metadata.set.identification-elements.element",
    "sampling_time": "om:samplingTime.gml:TimeInstant.gml:timePosition",
    "result_time": "om:resultTime.gml:TimeInstant.gml:timePosition",
}
