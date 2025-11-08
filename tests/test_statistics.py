"""Tests for Oura Ring statistics module."""
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.oura.statistics import (
    async_import_statistics,
    STATISTICS_METADATA,
    DATA_SOURCE_CONFIG,
    _parse_date_to_timestamp,
    _apply_transformation,
    _compute_percentage,
    _get_nested_value,
)


def test_statistics_metadata_completeness():
    """Test that all required sensors have metadata."""
    # These sensors should all have metadata
    required_sensors = [
        "sleep_score",
        "readiness_score",
        "activity_score",
        "steps",
        "vo2_max",
        "cardiovascular_age",
    ]
    
    for sensor in required_sensors:
        assert sensor in STATISTICS_METADATA
        metadata = STATISTICS_METADATA[sensor]
        assert "name" in metadata
        assert "has_mean" in metadata
        assert "has_sum" in metadata


def test_data_source_config_structure():
    """Test that data source configuration is properly structured."""
    for source_key, config in DATA_SOURCE_CONFIG.items():
        # Either has mappings or a custom processor
        assert "mappings" in config or "custom_processor" in config
        
        if "mappings" in config:
            assert isinstance(config["mappings"], list)
            
            for mapping in config["mappings"]:
                assert "sensor_key" in mapping
                assert "api_path" in mapping
                assert mapping["sensor_key"] in STATISTICS_METADATA


def test_timestamp_parsing():
    """Test that date strings are correctly parsed to timestamps."""
    # Test valid date
    timestamp = _parse_date_to_timestamp("2024-01-15")
    assert timestamp is not None
    assert timestamp.year == 2024
    assert timestamp.month == 1
    assert timestamp.day == 15
    assert timestamp.hour == 12  # Should be noon UTC
    assert timestamp.tzinfo == timezone.utc
    
    # Test invalid date
    assert _parse_date_to_timestamp(None) is None
    assert _parse_date_to_timestamp("") is None
    assert _parse_date_to_timestamp("invalid") is None


def test_value_transformations():
    """Test that data transformations work correctly."""
    # Test seconds to hours
    assert _apply_transformation(3600, "seconds_to_hours") == 1.0
    assert _apply_transformation(7200, "seconds_to_hours") == 2.0
    
    # Test seconds to minutes
    assert _apply_transformation(60, "seconds_to_minutes") == 1.0
    assert _apply_transformation(300, "seconds_to_minutes") == 5.0
    
    # Test percentage calculation
    assert _apply_transformation(30, "percentage", total=100) == 30.0
    
    # Test no transformation
    assert _apply_transformation(42, None) == 42


def test_compute_percentage():
    """Test percentage computation."""
    entry = {
        "total_sleep_duration": 28800,  # 8 hours
        "deep_sleep_duration": 7200,    # 2 hours = 25%
        "rem_sleep_duration": 5760,     # 1.6 hours = 20%
    }
    
    deep_pct = _compute_percentage(entry, "deep_sleep_duration", "total_sleep_duration")
    assert deep_pct == 25.0
    
    rem_pct = _compute_percentage(entry, "rem_sleep_duration", "total_sleep_duration")
    assert rem_pct == 20.0
    
    # Test missing values
    assert _compute_percentage({}, "numerator", "denominator") is None
    assert _compute_percentage({"numerator": 10}, "numerator", "denominator") is None
    assert _compute_percentage({"numerator": 10, "denominator": 0}, "numerator", "denominator") is None


def test_get_nested_value():
    """Test nested value extraction."""
    data = {
        "score": 85,
        "contributors": {
            "efficiency": 90,
            "restfulness": 75,
        },
    }
    
    # Test direct access
    assert _get_nested_value(data, "score") == 85
    
    # Test nested access
    assert _get_nested_value(data, "contributors.efficiency") == 90
    assert _get_nested_value(data, "contributors.restfulness") == 75
    
    # Test missing values
    assert _get_nested_value(data, "missing") is None
    assert _get_nested_value(data, "contributors.missing") is None
    assert _get_nested_value(data, "missing.nested") is None


