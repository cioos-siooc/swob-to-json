#!/bin/bash

# Create json files from xml files in test_files/input_xml

for i in test_files/input_xml/*.xml; do
    python -m swob_xml_to_json $i >$(dirname $i)/../output_json/$(basename $i).json
done
