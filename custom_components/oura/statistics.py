"""Import historical Oura data as Home Assistant Long-Term Statistics."""
from __future__ import annotations

from datetime import datetime, timezone
import logging
from typing import Any

from homeassistant.components.recorder.statistics import (
    async_add_external_statistics,
    StatisticData,
    StatisticMetaData,
)
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
    "sleep_score": {
        "name": "Sleep Score",
        "unit": "score",
        "has_mean": True,
        "has_sum": False,
    },
    "sleep_efficiency": {
        "name": "Sleep Efficiency",
        "unit": "score",
        "has_mean": True,
        "has_sum": False,
    },
    "restfulness": {
        "name": "Restfulness",
        "unit": "score",
        "has_mean": True,
        "has_sum": False,
    },
    "sleep_timing": {
        "name": "Sleep Timing",
        "unit": "score",
        "has_mean": True,
        "has_sum": False,
    },
    "total_sleep_duration": {
        "name": "Total Sleep Duration",
        "unit": UnitOfTime.HOURS,
        "has_mean": True,
        "has_sum": False,
    },
    "deep_sleep_duration": {
        "name": "Deep Sleep Duration",
        "unit": UnitOfTime.HOURS,
        "has_mean": True,
        "has_sum": False,
    },
    "rem_sleep_duration": {
        "name": "REM Sleep Duration",
        "unit": UnitOfTime.HOURS,
        "has_mean": True,
        "has_sum": False,
    },
    "light_sleep_duration": {
        "name": "Light Sleep Duration",
        "unit": UnitOfTime.HOURS,
        "has_mean": True,
        "has_sum": False,
    },
    "awake_time": {
        "name": "Awake Time",
        "unit": UnitOfTime.HOURS,
        "has_mean": True,
        "has_sum": False,
    },
    "sleep_latency": {
        "name": "Sleep Latency",
        "unit": UnitOfTime.MINUTES,
        "has_mean": True,
        "has_sum": False,
    },
    "time_in_bed": {
        "name": "Time in Bed",
        "unit": UnitOfTime.HOURS,
        "has_mean": True,
        "has_sum": False,
    },
    "deep_sleep_percentage": {
        "name": "Deep Sleep Percentage",
        "unit": "%",
        "has_mean": True,
        "has_sum": False,
    },
    "rem_sleep_percentage": {
        "name": "REM Sleep Percentage",
        "unit": "%",
        "has_mean": True,
        "has_sum": False,
    },
    "average_sleep_hrv": {
        "name": "Average Sleep HRV",
        "unit": "ms",
        "has_mean": True,
        "has_sum": False,
    },
    "readiness_score": {
        "name": "Readiness Score",
        "unit": "score",
        "has_mean": True,
        "has_sum": False,
    },
    "temperature_deviation": {
        "name": "Temperature Deviation",
        "unit": UnitOfTemperature.CELSIUS,
        "has_mean": True,
        "has_sum": False,
    },
    "resting_heart_rate": {
        "name": "Resting Heart Rate Score",
        "unit": "score",
        "has_mean": True,
        "has_sum": False,
    },
    "hrv_balance": {
        "name": "HRV Balance Score",
        "unit": "score",
        "has_mean": True,
        "has_sum": False,
    },
    "activity_score": {
        "name": "Activity Score",
        "unit": "score",
        "has_mean": True,
        "has_sum": False,
    },
    "steps": {
        "name": "Steps",
        "unit": "steps",
        "has_mean": False,
        "has_sum": True,
    },
    "active_calories": {
        "name": "Active Calories",
        "unit": UnitOfEnergy.KILO_CALORIE,
        "has_mean": False,
        "has_sum": True,
    },
    "total_calories": {
        "name": "Total Calories",
        "unit": UnitOfEnergy.KILO_CALORIE,
        "has_mean": False,
        "has_sum": True,
    },
    "target_calories": {
        "name": "Target Calories",
        "unit": UnitOfEnergy.KILO_CALORIE,
        "has_mean": True,
        "has_sum": False,
    },
    "met_min_high": {
        "name": "High Activity MET Minutes",
        "unit": "MET⋅min",
        "has_mean": False,
        "has_sum": True,
    },
    "met_min_medium": {
        "name": "Medium Activity MET Minutes",
        "unit": "MET⋅min",
        "has_mean": False,
        "has_sum": True,
    },
    "met_min_low": {
        "name": "Low Activity MET Minutes",
        "unit": "MET⋅min",
        "has_mean": False,
        "has_sum": True,
    },
    "average_heart_rate": {
        "name": "Average Heart Rate",
        "unit": "bpm",
        "has_mean": True,
        "has_sum": False,
    },
    "min_heart_rate": {
        "name": "Minimum Heart Rate",
        "unit": "bpm",
        "has_mean": True,
        "has_sum": False,
    },
    "max_heart_rate": {
        "name": "Maximum Heart Rate",
        "unit": "bpm",
        "has_mean": True,
        "has_sum": False,
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
    
    # Process each data type
    if sleep_data := data.get("sleep", {}).get("data"):
        stats_count = await _process_sleep_statistics(hass, sleep_data)
        total_stats += stats_count
        _LOGGER.debug("Imported %d sleep statistics", stats_count)
    
    if sleep_detail_data := data.get("sleep_detail", {}).get("data"):
        stats_count = await _process_sleep_detail_statistics(hass, sleep_detail_data)
        total_stats += stats_count
        _LOGGER.debug("Imported %d sleep detail statistics", stats_count)
    
    if readiness_data := data.get("readiness", {}).get("data"):
        stats_count = await _process_readiness_statistics(hass, readiness_data)
        total_stats += stats_count
        _LOGGER.debug("Imported %d readiness statistics", stats_count)
    
    if activity_data := data.get("activity", {}).get("data"):
        stats_count = await _process_activity_statistics(hass, activity_data)
        total_stats += stats_count
        _LOGGER.debug("Imported %d activity statistics", stats_count)
    
    if heartrate_data := data.get("heartrate", {}).get("data"):
        stats_count = await _process_heartrate_statistics(hass, heartrate_data)
        total_stats += stats_count
        _LOGGER.debug("Imported %d heart rate statistics", stats_count)
    
    _LOGGER.info("Successfully imported %d total statistics data points", total_stats)


async def _process_sleep_statistics(
    hass: HomeAssistant,
    sleep_data: list[dict[str, Any]],
) -> int:
    """Process sleep data and import as statistics."""
    stats_count = 0
    
    # Group data by sensor type
    sensor_data = {
        "sleep_score": [],
        "sleep_efficiency": [],
        "restfulness": [],
        "sleep_timing": [],
    }
    
    for entry in sleep_data:
        timestamp = _parse_date_to_timestamp(entry.get("day"))
        if not timestamp:
            continue
        
        score = entry.get("score")
        if score is not None:
            sensor_data["sleep_score"].append({"timestamp": timestamp, "value": score})
        
        if contributors := entry.get("contributors"):
            if efficiency := contributors.get("efficiency"):
                sensor_data["sleep_efficiency"].append({"timestamp": timestamp, "value": efficiency})
            if restfulness := contributors.get("restfulness"):
                sensor_data["restfulness"].append({"timestamp": timestamp, "value": restfulness})
            if timing := contributors.get("timing"):
                sensor_data["sleep_timing"].append({"timestamp": timestamp, "value": timing})
    
    # Import statistics for each sensor
    for sensor_key, data_points in sensor_data.items():
        if data_points:
            await _create_statistic(hass, sensor_key, data_points)
            stats_count += len(data_points)
    
    return stats_count


async def _process_sleep_detail_statistics(
    hass: HomeAssistant,
    sleep_detail_data: list[dict[str, Any]],
) -> int:
    """Process detailed sleep data and import as statistics."""
    stats_count = 0
    
    sensor_data = {
        "total_sleep_duration": [],
        "deep_sleep_duration": [],
        "rem_sleep_duration": [],
        "light_sleep_duration": [],
        "awake_time": [],
        "sleep_latency": [],
        "time_in_bed": [],
        "deep_sleep_percentage": [],
        "rem_sleep_percentage": [],
        "average_sleep_hrv": [],
    }
    
    for entry in sleep_detail_data:
        timestamp = _parse_date_to_timestamp(entry.get("day"))
        if not timestamp:
            continue
        
        # Process durations (convert seconds to hours)
        if total_sleep := entry.get("total_sleep_duration"):
            sensor_data["total_sleep_duration"].append({
                "timestamp": timestamp,
                "value": total_sleep / 3600
            })
        
        if deep_sleep := entry.get("deep_sleep_duration"):
            sensor_data["deep_sleep_duration"].append({
                "timestamp": timestamp,
                "value": deep_sleep / 3600
            })
        
        if rem_sleep := entry.get("rem_sleep_duration"):
            sensor_data["rem_sleep_duration"].append({
                "timestamp": timestamp,
                "value": rem_sleep / 3600
            })
        
        if light_sleep := entry.get("light_sleep_duration"):
            sensor_data["light_sleep_duration"].append({
                "timestamp": timestamp,
                "value": light_sleep / 3600
            })
        
        if awake := entry.get("awake_time"):
            sensor_data["awake_time"].append({
                "timestamp": timestamp,
                "value": awake / 3600
            })
        
        if latency := entry.get("latency"):
            sensor_data["sleep_latency"].append({
                "timestamp": timestamp,
                "value": latency / 60  # Convert to minutes
            })
        
        if time_in_bed := entry.get("time_in_bed"):
            sensor_data["time_in_bed"].append({
                "timestamp": timestamp,
                "value": time_in_bed / 3600
            })
        
        # Calculate percentages
        total_sleep_seconds = entry.get("total_sleep_duration")
        if total_sleep_seconds and total_sleep_seconds > 0:
            deep_sleep_seconds = entry.get("deep_sleep_duration")
            rem_sleep_seconds = entry.get("rem_sleep_duration")
            
            if deep_sleep_seconds is not None:
                percentage = (deep_sleep_seconds / total_sleep_seconds) * 100
                sensor_data["deep_sleep_percentage"].append({
                    "timestamp": timestamp,
                    "value": round(percentage, 1)
                })
            
            if rem_sleep_seconds is not None:
                percentage = (rem_sleep_seconds / total_sleep_seconds) * 100
                sensor_data["rem_sleep_percentage"].append({
                    "timestamp": timestamp,
                    "value": round(percentage, 1)
                })
        
        # HRV during sleep
        if hrv := entry.get("average_hrv"):
            sensor_data["average_sleep_hrv"].append({
                "timestamp": timestamp,
                "value": hrv
            })
    
    # Import statistics for each sensor
    for sensor_key, data_points in sensor_data.items():
        if data_points:
            await _create_statistic(hass, sensor_key, data_points)
            stats_count += len(data_points)
    
    return stats_count


async def _process_readiness_statistics(
    hass: HomeAssistant,
    readiness_data: list[dict[str, Any]],
) -> int:
    """Process readiness data and import as statistics."""
    stats_count = 0
    
    sensor_data = {
        "readiness_score": [],
        "temperature_deviation": [],
        "resting_heart_rate": [],
        "hrv_balance": [],
    }
    
    for entry in readiness_data:
        timestamp = _parse_date_to_timestamp(entry.get("day"))
        if not timestamp:
            continue
        
        if score := entry.get("score"):
            sensor_data["readiness_score"].append({"timestamp": timestamp, "value": score})
        
        if temp_dev := entry.get("temperature_deviation"):
            sensor_data["temperature_deviation"].append({"timestamp": timestamp, "value": temp_dev})
        
        if contributors := entry.get("contributors"):
            if rhr := contributors.get("resting_heart_rate"):
                sensor_data["resting_heart_rate"].append({"timestamp": timestamp, "value": rhr})
            if hrv := contributors.get("hrv_balance"):
                sensor_data["hrv_balance"].append({"timestamp": timestamp, "value": hrv})
    
    # Import statistics for each sensor
    for sensor_key, data_points in sensor_data.items():
        if data_points:
            await _create_statistic(hass, sensor_key, data_points)
            stats_count += len(data_points)
    
    return stats_count


async def _process_activity_statistics(
    hass: HomeAssistant,
    activity_data: list[dict[str, Any]],
) -> int:
    """Process activity data and import as statistics."""
    stats_count = 0
    
    sensor_data = {
        "activity_score": [],
        "steps": [],
        "active_calories": [],
        "total_calories": [],
        "target_calories": [],
        "met_min_high": [],
        "met_min_medium": [],
        "met_min_low": [],
    }
    
    for entry in activity_data:
        timestamp = _parse_date_to_timestamp(entry.get("day"))
        if not timestamp:
            continue
        
        if score := entry.get("score"):
            sensor_data["activity_score"].append({"timestamp": timestamp, "value": score})
        
        if steps := entry.get("steps"):
            sensor_data["steps"].append({"timestamp": timestamp, "value": steps})
        
        if active_cal := entry.get("active_calories"):
            sensor_data["active_calories"].append({"timestamp": timestamp, "value": active_cal})
        
        if total_cal := entry.get("total_calories"):
            sensor_data["total_calories"].append({"timestamp": timestamp, "value": total_cal})
        
        if target_cal := entry.get("target_calories"):
            sensor_data["target_calories"].append({"timestamp": timestamp, "value": target_cal})
        
        if met_high := entry.get("high_activity_met_minutes"):
            sensor_data["met_min_high"].append({"timestamp": timestamp, "value": met_high})
        
        if met_med := entry.get("medium_activity_met_minutes"):
            sensor_data["met_min_medium"].append({"timestamp": timestamp, "value": met_med})
        
        if met_low := entry.get("low_activity_met_minutes"):
            sensor_data["met_min_low"].append({"timestamp": timestamp, "value": met_low})
    
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
    """Process heart rate data and import daily statistics."""
    stats_count = 0
    
    # Group heart rate readings by day
    daily_readings: dict[str, list[int]] = {}
    
    for entry in heartrate_data:
        if bpm := entry.get("bpm"):
            # Extract date from timestamp (format: YYYY-MM-DDTHH:MM:SS+00:00)
            timestamp_str = entry.get("timestamp", "")
            if timestamp_str:
                day = timestamp_str.split("T")[0]  # Get just the date part
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
            "value": sum(readings) / len(readings)
        })
        sensor_data["min_heart_rate"].append({
            "timestamp": timestamp,
            "value": min(readings)
        })
        sensor_data["max_heart_rate"].append({
            "timestamp": timestamp,
            "value": max(readings)
        })
    
    # Import statistics for each sensor
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
    """Create and import a statistic for a sensor.
    
    Args:
        hass: Home Assistant instance
        sensor_key: Key identifying the sensor (e.g., "sleep_score")
        data_points: List of dicts with "timestamp" and "value" keys
    """
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
