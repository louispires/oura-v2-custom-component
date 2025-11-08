"""Tests for the OuraCoordinator data processing methods."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "custom_components"))

from oura.coordinator import OuraDataUpdateCoordinator


class MockCoordinator:
    """Mock coordinator for testing data processing methods without HA framework."""
    
    # Copy all the processing methods from the real coordinator
    _process_data = OuraDataUpdateCoordinator._process_data
    _process_sleep_scores = OuraDataUpdateCoordinator._process_sleep_scores
    _process_sleep_details = OuraDataUpdateCoordinator._process_sleep_details
    _process_readiness = OuraDataUpdateCoordinator._process_readiness
    _process_activity = OuraDataUpdateCoordinator._process_activity
    _process_heart_rate = OuraDataUpdateCoordinator._process_heart_rate
    _process_stress = OuraDataUpdateCoordinator._process_stress
    _process_resilience = OuraDataUpdateCoordinator._process_resilience
    _process_spo2 = OuraDataUpdateCoordinator._process_spo2
    _process_vo2_max = OuraDataUpdateCoordinator._process_vo2_max
    _process_cardiovascular_age = OuraDataUpdateCoordinator._process_cardiovascular_age
    _process_sleep_time = OuraDataUpdateCoordinator._process_sleep_time


def test_process_sleep_scores():
    """Test processing of sleep score data."""
    coordinator = MockCoordinator()
    data = {
        "sleep": {
            "data": [
                {
                    "score": 85,
                    "contributors": {
                        "efficiency": 90,
                        "restfulness": 80,
                        "timing": 75
                    }
                }
            ]
        }
    }
    processed = {}
    coordinator._process_sleep_scores(data, processed)
    
    assert processed["sleep_score"] == 85
    assert processed["sleep_efficiency"] == 90
    assert processed["restfulness"] == 80
    assert processed["sleep_timing"] == 75


def test_process_sleep_details_with_durations():
    """Test processing of sleep detail data with duration conversions."""
    coordinator = MockCoordinator()
    data = {
        "sleep_detail": {
            "data": [
                {
                    "total_sleep_duration": 28800,  # 8 hours in seconds
                    "deep_sleep_duration": 7200,    # 2 hours
                    "rem_sleep_duration": 7200,     # 2 hours
                    "light_sleep_duration": 14400,  # 4 hours
                    "awake_time": 1800,             # 0.5 hours
                    "latency": 600,                 # 10 minutes
                    "time_in_bed": 30600,           # 8.5 hours
                    "average_hrv": 45
                }
            ]
        }
    }
    processed = {}
    coordinator._process_sleep_details(data, processed)
    
    assert processed["total_sleep_duration"] == 8.0
    assert processed["deep_sleep_duration"] == 2.0
    assert processed["rem_sleep_duration"] == 2.0
    assert processed["light_sleep_duration"] == 4.0
    assert processed["awake_time"] == 0.5
    assert processed["sleep_latency"] == 10.0
    assert processed["time_in_bed"] == 8.5
    assert processed["average_sleep_hrv"] == 45
    assert processed["deep_sleep_percentage"] == 25.0
    assert processed["rem_sleep_percentage"] == 25.0


def test_process_readiness():
    """Test processing of readiness data."""
    coordinator = MockCoordinator()
    data = {
        "readiness": {
            "data": [
                {
                    "score": 82,
                    "temperature_deviation": -0.5,
                    "contributors": {
                        "resting_heart_rate": 85,
                        "hrv_balance": 90
                    }
                }
            ]
        }
    }
    processed = {}
    coordinator._process_readiness(data, processed)
    
    assert processed["readiness_score"] == 82
    assert processed["temperature_deviation"] == -0.5
    assert processed["resting_heart_rate"] == 85
    assert processed["hrv_balance"] == 90


def test_process_activity():
    """Test processing of activity data."""
    coordinator = MockCoordinator()
    data = {
        "activity": {
            "data": [
                {
                    "score": 88,
                    "steps": 12345,
                    "active_calories": 450,
                    "total_calories": 2200,
                    "target_calories": 500,
                    "high_activity_met_minutes": 120,
                    "medium_activity_met_minutes": 180,
                    "low_activity_met_minutes": 240
                }
            ]
        }
    }
    processed = {}
    coordinator._process_activity(data, processed)
    
    assert processed["activity_score"] == 88
    assert processed["steps"] == 12345
    assert processed["active_calories"] == 450
    assert processed["total_calories"] == 2200
    assert processed["target_calories"] == 500
    assert processed["met_min_high"] == 120
    assert processed["met_min_medium"] == 180
    assert processed["met_min_low"] == 240


def test_process_heart_rate_with_aggregation():
    """Test processing of heart rate data with aggregation."""
    coordinator = MockCoordinator()
    data = {
        "heartrate": {
            "data": [
                {"bpm": 55, "timestamp": "2024-01-01T00:00:00"},
                {"bpm": 58, "timestamp": "2024-01-01T00:05:00"},
                {"bpm": 62, "timestamp": "2024-01-01T00:10:00"},
                {"bpm": 60, "timestamp": "2024-01-01T00:15:00"},
                {"bpm": 57, "timestamp": "2024-01-01T00:20:00"}
            ]
        }
    }
    processed = {}
    coordinator._process_heart_rate(data, processed)
    
    assert processed["current_heart_rate"] == 57
    assert processed["heart_rate_timestamp"] == "2024-01-01T00:20:00"
    assert processed["average_heart_rate"] == (55 + 58 + 62 + 60 + 57) / 5
    assert processed["min_heart_rate"] == 55
    assert processed["max_heart_rate"] == 62


def test_process_stress():
    """Test processing of stress data."""
    coordinator = MockCoordinator()
    data = {
        "stress": {
            "data": [
                {
                    "stress_high_duration": 3600,
                    "recovery_high_duration": 1800,
                    "day_summary": "good"
                }
            ]
        }
    }
    processed = {}
    coordinator._process_stress(data, processed)
    
    assert processed["stress_high_duration"] == 3600
    assert processed["recovery_high_duration"] == 1800
    assert processed["stress_day_summary"] == "good"


def test_process_resilience():
    """Test processing of resilience data."""
    coordinator = MockCoordinator()
    data = {
        "resilience": {
            "data": [
                {
                    "level": "solid",
                    "sleep_recovery_score": 85,
                    "daytime_recovery_score": 78,
                    "contributors": {
                        "activity_score": 82
                    }
                }
            ]
        }
    }
    processed = {}
    coordinator._process_resilience(data, processed)
    
    assert processed["resilience_level"] == "solid"
    assert processed["sleep_recovery_score"] == 85
    assert processed["daytime_recovery_score"] == 78
    assert processed["stress_resilience_score"] == 82


def test_process_spo2():
    """Test processing of SpO2 data."""
    coordinator = MockCoordinator()
    data = {
        "spo2": {
            "data": [
                {
                    "spo2_percentage": {"average": 96.5},
                    "breathing_disturbance_index": 12
                }
            ]
        }
    }
    processed = {}
    coordinator._process_spo2(data, processed)
    
    assert processed["spo2_average"] == 96.5
    assert processed["breathing_disturbance_index"] == 12


def test_process_vo2_max():
    """Test processing of VO2 Max data."""
    coordinator = MockCoordinator()
    data = {
        "vo2_max": {
            "data": [{"vo2_max": 45.2}]
        }
    }
    processed = {}
    coordinator._process_vo2_max(data, processed)
    
    assert processed["vo2_max"] == 45.2


def test_process_cardiovascular_age():
    """Test processing of cardiovascular age data."""
    coordinator = MockCoordinator()
    data = {
        "cardiovascular_age": {
            "data": [{"age": 28}]
        }
    }
    processed = {}
    coordinator._process_cardiovascular_age(data, processed)
    
    assert processed["cardiovascular_age"] == 28


def test_process_sleep_time():
    """Test processing of sleep time recommendations."""
    coordinator = MockCoordinator()
    data = {
        "sleep_time": {
            "data": [
                {
                    "optimal_bedtime_start": "22:00:00",
                    "optimal_bedtime_end": "23:00:00"
                }
            ]
        }
    }
    processed = {}
    coordinator._process_sleep_time(data, processed)
    
    assert processed["optimal_bedtime_start"] == "22:00:00"
    assert processed["optimal_bedtime_end"] == "23:00:00"


def test_process_data_orchestration():
    """Test the main _process_data orchestration method."""
    coordinator = MockCoordinator()
    data = {
        "sleep": {"data": [{"score": 85, "contributors": {"efficiency": 90}}]},
        "activity": {"data": [{"score": 88, "steps": 12345}]},
        "readiness": {"data": [{"score": 82}]}
    }
    
    processed = coordinator._process_data(data)
    
    # Verify orchestration calls all relevant processors
    assert processed["sleep_score"] == 85
    assert processed["sleep_efficiency"] == 90
    assert processed["activity_score"] == 88
    assert processed["steps"] == 12345
    assert processed["readiness_score"] == 82


def test_empty_data_handling():
    """Test that empty data structures don't cause errors."""
    coordinator = MockCoordinator()
    data = {
        "sleep": {"data": []},
        "activity": {},
        "readiness": {"data": None}
    }
    
    processed = coordinator._process_data(data)
    
    # Should return empty dict without errors
    assert isinstance(processed, dict)
    assert len(processed) == 0
