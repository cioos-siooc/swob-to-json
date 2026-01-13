"""Unit tests for swob_to_json package."""

import json
import os
from pathlib import Path

import pytest

from swob_to_json import parseFile, parseText, parse_ccg_wind_direction, __version__
from swob_to_json.constants import (
    CCG_WIND_DIRECTION_MAP,
    INTEGER_KEY_SUFFIXES,
    MISSING_VALUE,
    NUMERIC_METADATA_FIELDS,
)
from swob_to_json.flatten_json import flatten_json, _extract_timestamp
from swob_to_json.ungroup_elements import ungroup_elements
from swob_to_json.swob_to_json import is_integer_key, replace_values


# Path to test files
TEST_FILES_DIR = Path(__file__).parent.parent / "test_files"
INPUT_DIR = TEST_FILES_DIR / "input_xml"
OUTPUT_DIR = TEST_FILES_DIR / "output_json"


class TestConstants:
    """Test the constants module."""

    def test_missing_value_is_string(self):
        assert isinstance(MISSING_VALUE, str)
        assert MISSING_VALUE == "MSNG"

    def test_numeric_metadata_fields(self):
        assert "lat" in NUMERIC_METADATA_FIELDS
        assert "long" in NUMERIC_METADATA_FIELDS
        assert "stn_elev" in NUMERIC_METADATA_FIELDS

    def test_integer_key_suffixes(self):
        assert "_code" in INTEGER_KEY_SUFFIXES
        assert "_summary" in INTEGER_KEY_SUFFIXES
        assert "_flag" in INTEGER_KEY_SUFFIXES

    def test_wind_direction_map_has_all_codes(self):
        # Should have codes 0-21
        for i in range(22):
            assert str(i) in CCG_WIND_DIRECTION_MAP


class TestWindDirection:
    """Test CCG wind direction code conversion."""

    def test_north(self):
        assert parse_ccg_wind_direction(8) == 0.0

    def test_south(self):
        assert parse_ccg_wind_direction(4) == 180.0

    def test_east(self):
        assert parse_ccg_wind_direction(2) == 90.0

    def test_west(self):
        assert parse_ccg_wind_direction(6) == 270.0

    def test_calm_returns_none(self):
        assert parse_ccg_wind_direction(0) is None

    def test_variable_returns_none(self):
        assert parse_ccg_wind_direction(9) is None

    def test_string_input(self):
        assert parse_ccg_wind_direction("8") == 0.0

    def test_invalid_code_returns_none(self):
        assert parse_ccg_wind_direction(99) is None
        assert parse_ccg_wind_direction("invalid") is None


class TestIsIntegerKey:
    """Test the is_integer_key helper function."""

    def test_code_suffix(self):
        assert is_integer_key("wnd_dir_code") is True
        assert is_integer_key("tot_cld_amt_code") is True

    def test_summary_suffix(self):
        assert is_integer_key("air_temp_qa_summary") is True

    def test_flag_suffix(self):
        assert is_integer_key("pcpn_amt_pst24hrs_data_flag") is True

    def test_non_integer_keys(self):
        assert is_integer_key("air_temp") is False
        assert is_integer_key("wnd_spd") is False
        assert is_integer_key("lat") is False

    def test_partial_match_not_enough(self):
        # Should only match at end, not substring
        assert is_integer_key("code_description") is False


class TestReplaceValues:
    """Test the replace_values utility function."""

    def test_replaces_matching_values(self):
        d = {"a": "MSNG", "b": 1.0, "c": "MSNG"}
        result = replace_values(d, "MSNG", None)
        assert result["a"] is None
        assert result["b"] == 1.0
        assert result["c"] is None

    def test_mutates_original(self):
        d = {"a": "MSNG"}
        result = replace_values(d, "MSNG", None)
        assert d is result
        assert d["a"] is None

    def test_no_match_unchanged(self):
        d = {"a": 1, "b": 2}
        replace_values(d, "MSNG", None)
        assert d == {"a": 1, "b": 2}


class TestUngroupElements:
    """Test the ungroup_elements function."""

    def test_none_returns_empty_dict(self):
        assert ungroup_elements(None) == {}

    def test_single_element_dict(self):
        # xmltodict returns dict for single element
        element = {"@name": "air_temp", "@value": "15.5"}
        result = ungroup_elements(element)
        assert result == {"air_temp": "15.5"}

    def test_list_of_elements(self):
        elements = [
            {"@name": "air_temp", "@value": "15.5"},
            {"@name": "rel_hum", "@value": "80.0"},
        ]
        result = ungroup_elements(elements)
        assert result == {"air_temp": "15.5", "rel_hum": "80.0"}

    def test_element_with_single_qualifier(self):
        element = {
            "@name": "wind_speed",
            "@value": "5.0",
            "qualifier": {"@name": "time_duration", "@value": "2"},
        }
        result = ungroup_elements(element)
        assert result == {
            "wind_speed": "5.0",
            "wind_speed_time_duration": "2",
        }

    def test_element_with_multiple_qualifiers(self):
        element = {
            "@name": "wind_speed",
            "@value": "5.0",
            "qualifier": [
                {"@name": "time_duration", "@value": "2"},
                {"@name": "vertical_displacement", "@value": "10"},
            ],
        }
        result = ungroup_elements(element)
        assert "wind_speed" in result
        assert "wind_speed_time_duration" in result
        assert "wind_speed_vertical_displacement" in result


class TestFlattenJson:
    """Test the flatten_json function."""

    def test_empty_data_returns_none_timestamps(self):
        result = flatten_json({})
        assert result["sampling_time"] is None
        assert result["result_time"] is None
        assert result["metadata"] == {}
        assert result["results"] == {}

    def test_extract_timestamp_missing_path(self):
        data = {"om:ObservationCollection": {}}
        result = _extract_timestamp(data, "om:samplingTime")
        assert result is None


class TestParseText:
    """Test the main parseText function."""

    def test_basic_xml_parsing(self):
        # Minimal valid SWOB XML
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <om:ObservationCollection xmlns:om="http://www.opengis.net/om/1.0"
                                   xmlns:gml="http://www.opengis.net/gml">
            <om:member>
                <om:Observation>
                    <om:samplingTime>
                        <gml:TimeInstant>
                            <gml:timePosition>2023-01-01T00:00:00.000Z</gml:timePosition>
                        </gml:TimeInstant>
                    </om:samplingTime>
                    <om:resultTime>
                        <gml:TimeInstant>
                            <gml:timePosition>2023-01-01T00:05:00.000Z</gml:timePosition>
                        </gml:TimeInstant>
                    </om:resultTime>
                    <om:metadata>
                        <set>
                            <identification-elements>
                                <element name="stn_id" value="TEST01"/>
                                <element name="lat" value="45.5"/>
                            </identification-elements>
                        </set>
                    </om:metadata>
                    <om:result>
                        <elements>
                            <element name="air_temp" value="20.5"/>
                            <element name="rel_hum" value="MSNG"/>
                        </elements>
                    </om:result>
                </om:Observation>
            </om:member>
        </om:ObservationCollection>
        """
        result = parseText(xml)

        assert result["sampling_time"] == "2023-01-01T00:00:00.000Z"
        assert result["result_time"] == "2023-01-01T00:05:00.000Z"
        assert result["metadata"]["stn_id"] == "TEST01"
        assert result["metadata"]["lat"] == 45.5  # Converted to float
        assert result["results"]["air_temp"] == 20.5  # Converted to float
        assert result["results"]["rel_hum"] is None  # MSNG replaced


class TestParseFileIntegration:
    """Integration tests using actual test files."""

    @pytest.fixture
    def input_files(self):
        """Get list of input XML files."""
        if not INPUT_DIR.exists():
            pytest.skip("Test input files not found")
        return list(INPUT_DIR.glob("*.xml"))

    def test_all_files_parse_without_error(self, input_files):
        """All test files should parse without raising exceptions."""
        for xml_file in input_files:
            result = parseFile(str(xml_file))
            assert "sampling_time" in result
            assert "result_time" in result
            assert "metadata" in result
            assert "results" in result

    def test_output_matches_expected(self):
        """Compare parsed output to expected JSON files."""
        if not OUTPUT_DIR.exists():
            pytest.skip("Test output files not found")

        for json_file in OUTPUT_DIR.glob("*.json"):
            # Find corresponding input file
            xml_filename = json_file.name.replace(".json", "")
            xml_file = INPUT_DIR / xml_filename

            if not xml_file.exists():
                continue

            with open(json_file) as f:
                expected = json.load(f)

            result = parseFile(str(xml_file))
            assert result == expected, f"Output mismatch for {xml_filename}"

    def test_ccg_wind_direction_conversion(self):
        """Test that CCG files have wind direction converted."""
        ccg_file = INPUT_DIR / "20230130T1140Z_DFO-CCG_SWOB_1018238.xml"
        if not ccg_file.exists():
            pytest.skip("CCG test file not found")

        result = parseFile(str(ccg_file))

        # Should have both the code and the converted direction
        assert "wnd_dir_code" in result["results"]
        assert "wnd_dir" in result["results"]
        # Code 8 = North = 0 degrees
        assert result["results"]["wnd_dir_code"] == 8
        assert result["results"]["wnd_dir"] == 0.0


class TestVersion:
    """Test version information."""

    def test_version_exists(self):
        assert __version__ is not None
        assert isinstance(__version__, str)

    def test_version_format(self):
        # Should be semantic versioning
        parts = __version__.split(".")
        assert len(parts) >= 2
        assert all(part.isdigit() for part in parts)
