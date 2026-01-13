[![Python package](https://github.com/cioos-siooc/swob-to-json/actions/workflows/test.yaml/badge.svg)](https://github.com/cioos-siooc/swob-to-json/actions/workflows/test.yaml)

# Surface Weather Markup Language (SWOB) to JSON

Converts [Environment and Climate Change Canada](https://www.canada.ca/en/environment-climate-change.html)'s [SWOB-ML XML](https://dd.weather.gc.ca/observations/swob-ml/) files to JSON.

SWOB is Surface Weather and Marine Observation Markup Language, the format is described in docs [here](https://dd.alpha.meteo.gc.ca/observations/doc)

## Installation

```bash
# Create a new python environment if required
python -m venv venv && source venv/bin/activate

# Install from GitHub
pip install --upgrade https://github.com/cioos-siooc/swob_to_json/tarball/main

# Or install with dev dependencies for testing
pip install -e ".[dev]"
```

Requires Python 3.10+.

## Command Line Usage

```bash
# Basic usage
python -m swob_to_json path/to/swob.xml

# With verbose logging (outputs to stderr)
python -m swob_to_json -v path/to/swob.xml

# Check version
python -m swob_to_json --version
```

See example output file: [test_files/output_json/2023-02-01-0615-46036-AUTO-swob.xml.json](https://raw.githubusercontent.com/cioos-siooc/swob_to_json/main/test_files/output_json/2023-02-01-0615-46036-AUTO-swob.xml.json)

## Module Usage

```python
from swob_to_json import parseFile, parseText

# Parse from file
result = parseFile("path/to/swob.xml")

# Parse from XML string
result = parseText(xml_string)
```

### Output Structure

```python
{
    "sampling_time": "2023-01-01T00:00:00.000Z",  # ISO timestamp of observation
    "result_time": "2023-01-01T00:05:00.000Z",    # ISO timestamp when recorded
    "metadata": {
        "stn_id": "TEST01",
        "lat": 45.5,        # Converted to float
        "long": -75.0,      # Converted to float
        "stn_elev": 100.0,  # Converted to float
        # ... other station metadata
    },
    "results": {
        "air_temp": 20.5,              # Converted to float
        "air_temp_qa_summary": 100,    # Integer (ends with _summary)
        "wnd_dir_code": 8,             # Integer (ends with _code)
        "wnd_dir": 0.0,                # Converted from code to degrees
        # ... other observation values
    }
}
```

### Wind Direction Conversion

For Canadian Coast Guard (CCG) observations, the `wnd_dir_code` field contains a coded direction (0-21). The parser automatically converts this to compass degrees in a new `wnd_dir` field.

```python
from swob_to_json import parse_ccg_wind_direction

degrees = parse_ccg_wind_direction(8)  # Returns 0.0 (North)
degrees = parse_ccg_wind_direction(4)  # Returns 180.0 (South)
degrees = parse_ccg_wind_direction(0)  # Returns None (Calm)
```

## Docker Usage

```bash
# Build the image
docker build -t swob-to-json .

# Run conversion on test files
docker run -v $(pwd)/output:/output_json swob-to-json
```

## Testing

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run type checking
mypy swob_to_json/
```

## Links

- [ECCC Datamart SWOB-ML folder](https://dd.weather.gc.ca/observations/swob-ml/)
- [ECCC SWOB Docs](https://dd.weather.gc.ca/observations/doc)
- [ECCC](https://www.canada.ca/en/environment-climate-change.html)
