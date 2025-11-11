"""Import historical Oura data as Home Assistant Long-Term Statistics.

This module provides a configuration-driven approach to importing Oura Ring data
as Home Assistant long-term statistics, significantly reducing code duplication.
"""
from __future__ import annotations

from datetime import datetime, timezone
import logging
from typing import Any, Callable

from homeassistant.components.recorder.statistics import (
    async_add_external_statistics,
    StatisticData,
    StatisticMetaData,
)
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.const import (
    UnitOfTemperature,
    UnitOfTime,
    UnitOfEnergy,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Statistics metadata for all Oura sensors
STATISTICS_METADATA = {
    "sleep_score": {"name": "Sleep Score", "unit": "score", "has_mean": True, "has_sum": False},
    "sleep_efficiency": {"name": "Sleep Efficiency", "unit": "score", "has_mean": True, "has_sum": False},
    "restfulness": {"name": "Restfulness", "unit": "score", "has_mean": True, "has_sum": False},
    "sleep_timing": {"name": "Sleep Timing", "unit": "score", "has_mean": True, "has_sum": False},
    "total_sleep_duration": {"name": "Total Sleep Duration", "unit": UnitOfTime.HOURS, "has_mean": True, "has_sum": False},
    "deep_sleep_duration": {"name": "Deep Sleep Duration", "unit": UnitOfTime.HOURS, "has_mean": True, "has_sum": False},
    "rem_sleep_duration": {"name": "REM Sleep Duration", "unit": UnitOfTime.HOURS, "has_mean": True, "has_sum": False},
    "light_sleep_duration": {"name": "Light Sleep Duration", "unit": UnitOfTime.HOURS, "has_mean": True, "has_sum": False},
    "awake_time": {"name": "Awake Time", "unit": UnitOfTime.HOURS, "has_mean": True, "has_sum": False},
    "sleep_latency": {"name": "Sleep Latency", "unit": UnitOfTime.MINUTES, "has_mean": True, "has_sum": False},
    "time_in_bed": {"name": "Time in Bed", "unit": UnitOfTime.HOURS, "has_mean": True, "has_sum": False},
    "deep_sleep_percentage": {"name": "Deep Sleep Percentage", "unit": "%", "has_mean": True, "has_sum": False},
    "rem_sleep_percentage": {"name": "REM Sleep Percentage", "unit": "%", "has_mean": True, "has_sum": False},
    "average_sleep_hrv": {"name": "Average Sleep HRV", "unit": "ms", "has_mean": True, "has_sum": False},
    "readiness_score": {"name": "Readiness Score", "unit": "score", "has_mean": True, "has_sum": False},
    "temperature_deviation": {"name": "Temperature Deviation", "unit": UnitOfTemperature.CELSIUS, "has_mean": True, "has_sum": False},
    "resting_heart_rate": {"name": "Resting Heart Rate Score", "unit": "score", "has_mean": True, "has_sum": False},
    "hrv_balance": {"name": "HRV Balance Score", "unit": "score", "has_mean": True, "has_sum": False},
    "activity_score": {"name": "Activity Score", "unit": "score", "has_mean": True, "has_sum": False},
    "steps": {"name": "Steps", "unit": "steps", "has_mean": False, "has_sum": True},
    "active_calories": {"name": "Active Calories", "unit": UnitOfEnergy.KILO_CALORIE, "has_mean": False, "has_sum": True},
    "total_calories": {"name": "Total Calories", "unit": UnitOfEnergy.KILO_CALORIE, "has_mean": False, "has_sum": True},
    "target_calories": {"name": "Target Calories", "unit": UnitOfEnergy.KILO_CALORIE, "has_mean": True, "has_sum": False},
    "met_min_high": {"name": "High Activity MET Minutes", "unit": "METâ‹…min", "has_mean": False, "has_sum": True},
    "met_min_medium": {"name": "Medium Activity MET Minutes", "unit": "METâ‹…min", "has_mean": False, "has_sum": True},
    "met_min_low": {"name": "Low Activity MET Minutes", "unit": "METâ‹…min", "has_mean": False, "has_sum": True},
    "average_heart_rate": {"name": "Average Heart Rate", "unit": "bpm", "has_mean": True, "has_sum": False},
    "min_heart_rate": {"name": "Minimum Heart Rate", "unit": "bpm", "has_mean": True, "has_sum": False},
    "max_heart_rate": {"name": "Maximum Heart Rate", "unit": "bpm", "has_mean": True, "has_sum": False},
    "stress_high_duration": {"name": "Stress High Duration", "unit": UnitOfTime.MINUTES, "has_mean": True, "has_sum": False},
    "recovery_high_duration": {"name": "Recovery High Duration", "unit": UnitOfTime.MINUTES, "has_mean": True, "has_sum": False},
    "stress_day_summary": {"name": "Stress Day Summary", "unit": None, "has_mean": False, "has_sum": False},
    "resilience_level": {"name": "Resilience Level", "unit": None, "has_mean": False, "has_sum": False},
    "sleep_recovery_score": {"name": "Sleep Recovery Score", "unit": "score", "has_mean": True, "has_sum": False},
    "daytime_recovery_score": {"name": "Daytime Recovery Score", "unit": "score", "has_mean": True, "has_sum": False},
    "stress_resilience_score": {"name": "Stress Resilience Score", "unit": "score", "has_mean": True, "has_sum": False},
    "spo2_average": {"name": "SpO2 Average", "unit": "%", "has_mean": True, "has_sum": False},
    "breathing_disturbance_index": {"name": "Breathing Disturbance Index", "unit": None, "has_mean": True, "has_sum": False},
    "vo2_max": {"name": "VO2 Max", "unit": "ml/kg/min", "has_mean": True, "has_sum": False},
    "cardiovascular_age": {"name": "Cardiovascular Age", "unit": "years", "has_mean": True, "has_sum": False},
    "optimal_bedtime_start": {"name": "Optimal Bedtime Start", "unit": None, "has_mean": False, "has_sum": False},
    "optimal_bedtime_end": {"name": "Optimal Bedtime End", "unit": None, "has_mean": False, "has_sum": False},
}

# Configuration mapping API data sources to sensor mappings
DATA_SOURCE_CONFIG = {
    "sleep": {
        "mappings": [
            {"sensor_key": "sleep_score", "api_path": "score"},
            {"sensor_key": "sleep_efficiency", "api_path": "contributors.efficiency"},
            {"sensor_key": "restfulness", "api_path": "contributors.restfulness"},
            {"sensor_key": "sleep_timing", "api_path": "contributors.timing"},
        ],
    },
    "sleep_detail": {
        "mappings": [
            {"sensor_key": "total_sleep_duration", "api_path": "total_sleep_duration", "transform": "seconds_to_hours"},
            {"sensor_key": "deep_sleep_duration", "api_path": "deep_sleep_duration", "transform": "seconds_to_hours"},
            {"sensor_key": "rem_sleep_duration", "api_path": "rem_sleep_duration", "transform": "seconds_to_hours"},
            {"sensor_key": "light_sleep_duration", "api_path": "light_sleep_duration", "transform": "seconds_to_hours"},
            {"sensor_key": "awake_time", "api_path": "awake_time", "transform": "seconds_to_hours"},
            {"sensor_key": "sleep_latency", "api_path": "latency", "transform": "seconds_to_minutes"},
            {"sensor_key": "time_in_bed", "api_path": "time_in_bed", "transform": "seconds_to_hours"},
            {"sensor_key": "average_sleep_hrv", "api_path": "average_hrv"},
        ],
        "computed": [
            {
                "sensor_key": "deep_sleep_percentage",
                "compute": lambda entry: _compute_percentage(entry, "deep_sleep_duration", "total_sleep_duration"),
            },
            {
                "sensor_key": "rem_sleep_percentage",
                "compute": lambda entry: _compute_percentage(entry, "rem_sleep_duration", "total_sleep_duration"),
            },
        ],
    },
    "readiness": {
        "mappings": [
            {"sensor_key": "readiness_score", "api_path": "score"},
            {"sensor_key": "temperature_deviation", "api_path": "temperature_deviation"},
            {"sensor_key": "resting_heart_rate", "api_path": "contributors.resting_heart_rate"},
            {"sensor_key": "hrv_balance", "api_path": "contributors.hrv_balance"},
        ],
    },
    "activity": {
        "mappings": [
            {"sensor_key": "activity_score", "api_path": "score"},
            {"sensor_key": "steps", "api_path": "steps"},
            {"sensor_key": "active_calories", "api_path": "active_calories"},
            {"sensor_key": "total_calories", "api_path": "total_calories"},
            {"sensor_key": "target_calories", "api_path": "target_calories"},
            {"sensor_key": "met_min_high", "api_path": "high_activity_met_minutes"},
            {"sensor_key": "met_min_medium", "api_path": "medium_activity_met_minutes"},
            {"sensor_key": "met_min_low", "api_path": "low_activity_met_minutes"},
        ],
    },
    "heartrate": {
        "custom_processor": "_process_heartrate_statistics",
    },
    "stress": {
        "mappings": [
            {"sensor_key": "stress_high_duration", "api_path": "stress_high_duration"},
            {"sensor_key": "recovery_high_duration", "api_path": "recovery_high_duration"},
            {"sensor_key": "stress_day_summary", "api_path": "day_summary"},
        ],
    },
    "resilience": {
        "mappings": [
            {"sensor_key": "resilience_level", "api_path": "level"},
            {"sensor_key": "sleep_recovery_score", "api_path": "sleep_recovery_score"},
            {"sensor_key": "daytime_recovery_score", "api_path": "daytime_recovery_score"},
            {"sensor_key": "stress_resilience_score", "api_path": "contributors.activity_score"},
        ],
    },
    "spo2": {
        "mappings": [
            {"sensor_key": "spo2_average", "api_path": "average"},
            {"sensor_key": "breathing_disturbance_index", "api_path": "breathing_disturbance_index"},
        ],
    },
    "vo2_max": {
        "mappings": [
            {"sensor_key": "vo2_max", "api_path": "vo2_max"},
        ],
    },
    "cardiovascular_age": {
        "mappings": [
            {"sensor_key": "cardiovascular_age", "api_path": "age"},
        ],
    },
    "sleep_time": {
        "mappings": [
            {"sensor_key": "optimal_bedtime_start", "api_path": "optimal_bedtime_start"},
            {"sensor_key": "optimal_bedtime_end", "api_path": "optimal_bedtime_end"},
        ],
    },
}


async def async_import_statistics(
    hass: HomeAssistant,
    data: dict[str, Any],
) -> None:
    """Import historical Oura data as long-term statistics.
    
    Args:
        hass: Home Assistant instance
        data: Historical data from Oura API
    """
    _LOGGER.info("Starting statistics import from historical data")
    
    total_stats = 0
    
    # Process each configured data source
    for source_key, config in DATA_SOURCE_CONFIG.items():
        source_data = data.get(source_key, {}).get("data")
        if not source_data:
            continue
        
        # Check if custom processor is specified
        if custom_processor := config.get("custom_processor"):
            processor_func = globals().get(custom_processor)
            if processor_func:
                stats_count = await processor_func(hass, source_data)
                total_stats += stats_count
                _LOGGER.debug("Imported %d %s statistics", stats_count, source_key)
            continue
        
        # Use generic processor
        stats_count = await _process_generic_statistics(hass, source_data, config)
        total_stats += stats_count
        _LOGGER.debug("Imported %d %s statistics", stats_count, source_key)
    
    _LOGGER.info("Successfully imported %d total statistics data points", total_stats)


async def _process_generic_statistics(
    hass: HomeAssistant,
    data_list: list[dict[str, Any]],
    config: dict[str, Any],
) -> int:
    """Process data using generic configuration-driven approach.
    
    Args:
        hass: Home Assistant instance
        data_list: List of data entries from API
        config: Configuration with mappings and computed fields
    
    Returns:
        Number of statistics imported
    """
    stats_count = 0
    
    # Initialize data collectors for each sensor
    sensor_data: dict[str, list[dict[str, Any]]] = {}
    for mapping in config.get("mappings", []):
        sensor_data[mapping["sensor_key"]] = []
    
    for computed in config.get("computed", []):
        sensor_data[computed["sensor_key"]] = []
    
    # Process each data entry
    for entry in data_list:
        timestamp = _parse_date_to_timestamp(entry.get("day"))
        if not timestamp:
            continue
        
        # Process direct mappings
        for mapping in config.get("mappings", []):
            value = _get_nested_value(entry, mapping["api_path"])
            if value is not None:
                # Apply transformation if specified
                if transform := mapping.get("transform"):
                    value = _apply_transformation(value, transform)
                
                sensor_data[mapping["sensor_key"]].append({
                    "timestamp": timestamp,
                    "value": value,
                })
        
        # Process computed fields
        for computed in config.get("computed", []):
            value = computed["compute"](entry)
            if value is not None:
                sensor_data[computed["sensor_key"]].append({
                    "timestamp": timestamp,
                    "value": value,
                })
    
    # Import statistics for each sensor
    for sensor_key, data_points in sensor_data.items():
        if data_points:
            await _create_statistic(hass, sensor_key, data_points)
            stats_count += len(data_points)
    
    return stats_count


async def _process_heartrate_statistics(
    hass: HomeAssistant,
    heartrate_data: list[dict[str, Any]],
) -> int:
    """Process heart rate data with special daily aggregation logic.
    
    Heart rate data comes as individual readings throughout the day,
    so we need to aggregate them into daily statistics.
    """
    stats_count = 0
    
    # Group heart rate readings by day
    daily_readings: dict[str, list[int]] = {}
    
    for entry in heartrate_data:
        if bpm := entry.get("bpm"):
            # Extract date from timestamp
            timestamp_str = entry.get("timestamp", "")
            if timestamp_str:
                day = timestamp_str.split("T")[0]
                if day not in daily_readings:
                    daily_readings[day] = []
                daily_readings[day].append(bpm)
    
    # Calculate daily statistics
    sensor_data = {
        "average_heart_rate": [],
        "min_heart_rate": [],
        "max_heart_rate": [],
    }
    
    for day, readings in daily_readings.items():
        timestamp = _parse_date_to_timestamp(day)
        if not timestamp or not readings:
            continue
        
        sensor_data["average_heart_rate"].append({
            "timestamp": timestamp,
            "value": sum(readings) / len(readings),
        })
        sensor_data["min_heart_rate"].append({
            "timestamp": timestamp,
            "value": min(readings),
        })
        sensor_data["max_heart_rate"].append({
            "timestamp": timestamp,
            "value": max(readings),
        })
    
    # Import statistics
    for sensor_key, data_points in sensor_data.items():
        if data_points:
            await _create_statistic(hass, sensor_key, data_points)
            stats_count += len(data_points)
    
    return stats_count


async def _create_statistic(
    hass: HomeAssistant,
    sensor_key: str,
    data_points: list[dict[str, Any]],
) -> None:
    """Create and import a statistic for a sensor."""
    if not data_points:
        return
    
    metadata = STATISTICS_METADATA.get(sensor_key)
    if not metadata:
        _LOGGER.warning("No metadata found for sensor: %s", sensor_key)
        return
    
    statistic_id = f"{DOMAIN}:{sensor_key}"
    
    # Create metadata
    stat_metadata = StatisticMetaData(
        has_mean=metadata["has_mean"],
        has_sum=metadata["has_sum"],
        name=metadata["name"],
        source=DOMAIN,
        statistic_id=statistic_id,
        unit_of_measurement=metadata["unit"],
        unit_class=SensorDeviceClass.MEASUREMENT if metadata["has_mean"] else None,
    )
    
    # Create data points
    statistics = []
    for point in data_points:
        stat_data = StatisticData(
            start=point["timestamp"],
            mean=point["value"] if metadata["has_mean"] else None,
            sum=point["value"] if metadata["has_sum"] else None,
        )
        statistics.append(stat_data)
    
    # Import to database
    async_add_external_statistics(hass, stat_metadata, statistics)
    _LOGGER.debug(
        "Imported %d statistics for %s (%s)",
        len(statistics),
        metadata["name"],
        sensor_key,
    )


def _get_nested_value(data: dict[str, Any], path: str) -> Any:
    """Get a value from nested dictionary using dot notation.
    
    Args:
        data: Dictionary to extract from
        path: Dot-separated path (e.g., "contributors.efficiency")
    
    Returns:
        Value at path, or None if not found
    """
    keys = path.split(".")
    value = data
    
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
            if value is None:
                return None
        else:
            return None
    
    return value


def _apply_transformation(value: Any, transform: str, **kwargs) -> Any:
    """Apply a transformation to a value.
    
    Args:
        value: Value to transform
        transform: Transformation name
        **kwargs: Additional arguments for transformation
    
    Returns:
        Transformed value
    """
    if transform == "seconds_to_hours":
        return value / 3600
    elif transform == "seconds_to_minutes":
        return value / 60
    elif transform == "percentage":
        total = kwargs.get("total", 100)
        return (value / total) * 100 if total else 0
    
    return value


def _compute_percentage(entry: dict[str, Any], numerator_key: str, denominator_key: str) -> float | None:
    """Compute a percentage from two entry fields.
    
    Args:
        entry: Data entry
        numerator_key: Key for numerator value
        denominator_key: Key for denominator value
    
    Returns:
        Percentage value rounded to 1 decimal, or None if can't compute
    """
    numerator = entry.get(numerator_key)
    denominator = entry.get(denominator_key)
    
    if numerator is None or denominator is None or denominator == 0:
        return None
    
    return round((numerator / denominator) * 100, 1)


def _parse_date_to_timestamp(date_str: str | None) -> datetime | None:
    """Parse ISO date string to datetime object.
    
    Args:
        date_str: ISO format date string (e.g., "2024-01-15")
    
    Returns:
        Datetime object in UTC timezone, or None if parsing fails
    """
    if not date_str:
        return None
    
    try:
        # Parse the date string and set time to noon UTC
        # This ensures statistics appear on the correct day in all timezones
        date_parts = date_str.split("T")[0].split("-")
        year, month, day = int(date_parts[0]), int(date_parts[1]), int(date_parts[2])
        return datetime(year, month, day, 12, 0, 0, tzinfo=timezone.utc)
    except (ValueError, IndexError) as err:
        _LOGGER.warning("Failed to parse date '%s': %s", date_str, err)
        return None
