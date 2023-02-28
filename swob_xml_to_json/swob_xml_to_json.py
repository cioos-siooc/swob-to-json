#!/usr/bin/env python3
from swob_xml_to_json.flatten_json import flatten_json

import xmltodict

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

def parse(xml_file_path):
    """
    Converts XML to JSON
    """

    with open(xml_file_path, "r") as content_file:
        xml_string = content_file.read()

    data_dict =  xmltodict.parse(xml_string)

    # parse out a flat dictionary of the data/metadata fields
    record = flatten_json(data_dict)

    # remove fill values
    replace_values(record, "MSNG", None)
    return record


