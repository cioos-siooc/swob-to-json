#!/usr/bin/env python3
import xmltodict

from swob_to_json.flatten_json import flatten_json

"""

Parse XML from swob-ml and flatten

"""


def replace_values(input_dict, from_value, to_value):
    """
    Replaces values at top level of dictionary. Mutates source dictionary. Non-recursive
    """
    for key, val in input_dict.items():
        if val == from_value:
            input_dict[key] = to_value
    return input_dict


def parseFile(xml_file_path):
    with open(xml_file_path, "r") as content_file:
        xml_string = content_file.read()
    return parseText(xml_string)


def parse_ccg_wind_direction(value: int) -> float:
    directions = {
        "0": None,  # Calm
        "1": 45,  # Northeast (NE)
        "2": 90,  # East (E)
        "3": 135,  # Southeast (SE)
        "4": 180,  # South (S)
        "5": 225,  # Southwest (SW)
        "6": 270,  # West (W)
        "7": 315,  # Northwest (NW)
        "8": 0,  # North (N) - Changed from 360 to 0
        "9": None,  # Variable/All directions/confused/unknown
        "10": None,  # Not reported
        "11": None,  # Ship in shore or flaw lead
        "12": None,  # Not determined (ship in ice)
        "13": None,  # Unable to report due to darkness, etc.
        "14": 22.5,  # North-northeast (NNE)
        "15": 67.5,  # East-northeast (ENE)
        "16": 112.5,  # East-southeast (ESE)
        "17": 157.5,  # South-southeast (SSE)
        "18": 202.5,  # South-southwest (SSW)
        "19": 247.5,  # West-southwest (WSW)
        "20": 292.5,  # West-northwest (WNW)
        "21": 337.5,  # North-northwest (NNW)
    }

    return directions.get(str(value), None)


def is_integer_key(key: str) -> bool:
    integer_keys = ["_code", "_summary", "_flag"]
    for integer_key in integer_keys:
        if integer_key in key:
            return True
    return False


def parseText(xml_string):
    """
    Converts XML to JSON
    """

    data_dict = xmltodict.parse(xml_string)

    # parse out a flat dictionary of the data/metadata fields
    record = flatten_json(data_dict)

    # remove fill values
    replace_values(record["results"], "MSNG", None)

    # convert results to numeric
    for key, value in record["results"].items():
        try:
            # code, flag, and summary are integers
            if is_integer_key(key):
                record["results"][key] = int(value)
            else:
                record["results"][key] = float(value)
        except:
            pass

    # convert a few metadata fields to numeric
    for key, value in record["metadata"].items():
        try:
            if key in ["lat", "long", "stn_elev"]:
                record["metadata"][key] = float(value)
        except:
            pass

    replace_values(record["metadata"], "MSNG", None)

    # check for ccg wind direction wnd_dir_code
    # and convert to degrees
    if "wnd_dir_code" in record["results"]:
        record["results"]["wnd_dir"] = parse_ccg_wind_direction(
            str(int(record["results"]["wnd_dir_code"]))
        )
    return record
