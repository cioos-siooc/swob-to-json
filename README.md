# SWOB XML to JSON

Converts Environment and Climate Change Canada's SWOB-ML XML files to JSON.

SWOB is Surface Weather and Marine Observation Markup Language

## Installation/CLI Usage

1. Clone this repo
1. Create a new python environment if required
1. `pip install .`
1. python -m swob_xml_to_json test_files/input/2023-02-01-0615-46036-AUTO-swob.xml

## Usage as module

```python
from swob_xml_to_json import swob_xml_to_json

swob_json = swob_xml_to_json.parse(filename)

```

## Links

- [ECCC Datamart SWOB-ML folder](https://dd.weather.gc.ca/observations/swob-ml/)
- [ECCC SWOB Docs](https://dd.alpha.meteo.gc.ca/observations/doc)
- [ECCC](https://www.canada.ca/en/environment-climate-change.html)
