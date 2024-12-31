[![Python package](https://github.com/cioos-siooc/swob_xml_to_json/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/cioos-siooc/swob_xml_to_json/actions/workflows/test.yaml)

# SWOB XML to JSON

Converts [Environment and Climate Change Canada](https://www.canada.ca/en/environment-climate-change.html)'s [SWOB-ML XML](https://dd.weather.gc.ca/observations/swob-ml/) files to JSON.

SWOB is Surface Weather and Marine Observation Markup Language, the format is described in docs [here](https://dd.alpha.meteo.gc.ca/observations/doc)

## Installation

1. Create a new python environment if required. eg `python -m venv venv && source venv/bin/activate`
1. `pip install --upgrade https://github.com/cioos-siooc/swob_xml_to_json/tarball/main`

## Command line usage

1. python -m swob_xml_to_json [/test_files/input_xml/2023-02-01-0615-46036-AUTO-swob.xml](https://raw.githubusercontent.com/cioos-siooc/swob_xml_to_json/main/test_files/input_xml/2023-02-01-0615-46036-AUTO-swob.xml)
1. See example output file - [/test_files/output_json/2023-02-01-0615-46036-AUTO-swob.xml.json](https://raw.githubusercontent.com/cioos-siooc/swob_xml_to_json/main/test_files/output_json/2023-02-01-0615-46036-AUTO-swob.xml.json)

## Module Usage

```python
from swob_xml_to_json import swob_xml_to_json

swob_json = swob_xml_to_json.parseFile(filename)
# or
swob_json = swob_xml_to_json.parseText(xml_string)

```

## Links

- [ECCC Datamart SWOB-ML folder](https://dd.weather.gc.ca/observations/swob-ml/)
- [ECCC SWOB Docs](https://dd.weather.gc.ca/observations/doc)
- [ECCC](https://www.canada.ca/en/environment-climate-change.html)
