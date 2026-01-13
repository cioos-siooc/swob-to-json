# CLAUDE.md

This file provides context for Claude Code when working on this project.

## Project Overview

**swob-to-json** converts SWOB-ML (Surface Weather and Marine Observation Markup Language) XML files from Environment and Climate Change Canada (ECCC) into flat JSON format suitable for tabular data processing.

## Architecture

```
swob_to_json/
├── __init__.py         # Public API exports (parseFile, parseText, parse_ccg_wind_direction)
├── __main__.py         # CLI entry point (click-based, supports -v and --version)
├── swob_to_json.py     # Main parsing logic and numeric conversion
├── flatten_json.py     # Extracts data from nested XML structure
├── ungroup_elements.py # Converts <element>/<qualifier> tags to key-value pairs
├── constants.py        # Magic values, field mappings, wind direction codes
└── py.typed            # PEP 561 marker for type checking support
```

### Data Flow

1. XML string → `xmltodict.parse()` → nested dict
2. `flatten_json()` extracts results, metadata, and timestamps
3. `ungroup_elements()` flattens `<element>` tags with qualifiers
4. `parseText()` converts numeric fields and replaces "MSNG" with None
5. CCG wind direction codes are converted to compass degrees

## Key Constants (in constants.py)

- `MISSING_VALUE = "MSNG"` - Fill value for missing data
- `INTEGER_KEY_SUFFIXES = ("_code", "_summary", "_flag")` - Fields parsed as int
- `NUMERIC_METADATA_FIELDS = {"lat", "long", "stn_elev"}` - Metadata parsed as float
- `CCG_WIND_DIRECTION_MAP` - Codes 0-21 → compass degrees

## Common Tasks

### Running Tests
```bash
pytest tests/ -v
```

### Testing a Single File
```bash
python -m swob_to_json test_files/input_xml/2023-02-01-0615-46036-AUTO-swob.xml
```

### Verbose Mode (Debug Logging)
```bash
python -m swob_to_json -v path/to/file.xml
```

### Regenerating Expected Test Outputs
```bash
for f in test_files/input_xml/*.xml; do
  python -m swob_to_json "$f" > "test_files/output_json/$(basename "$f").json"
done
```

### Type Checking
```bash
mypy swob_to_json/
```

### Building Docker Image
```bash
docker build -t swob-to-json .
docker run -v $(pwd)/output:/output_json swob-to-json
```

## Project Configuration

- **pyproject.toml** - Main project config (dependencies, metadata, tool settings)
- **setup.py** - Minimal shim for backward compatibility
- **.github/workflows/test.yaml** - CI testing on Python 3.10 and 3.14
- **Dockerfile** - Uses Python 3.14-slim

## Dependencies

- `click` - CLI framework
- `xmltodict` - XML parsing
- `pytest` (dev) - Testing
- `mypy` (dev) - Type checking

## Notes

- The `xmltodict` library returns a dict for single elements but a list for multiple elements. Code must handle both cases.
- All numeric conversion failures are logged at DEBUG level and the original value is preserved.
- Timestamps may be None if the XML structure is malformed.
- Package is PEP 561 compliant (includes py.typed marker).
