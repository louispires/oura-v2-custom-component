"""Constants for the Oura Ring integration."""
from datetime import timedelta
from typing import Final

DOMAIN: Final = "oura"
ATTRIBUTION: Final = "Data provided by Oura Ring"

# Configuration
CONF_UPDATE_INTERVAL: Final = "update_interval"
CONF_HISTORICAL_DAYS: Final = "historical_days"

# OAuth2 Constants
OAUTH2_AUTHORIZE: Final = "https://cloud.ouraring.com/oauth/authorize"
OAUTH2_TOKEN: Final = "https://api.ouraring.com/oauth/token"
OAUTH2_SCOPES: Final = [
    "email",
    "personal",
    "daily",
    "heartrate",
    "workout",
    "session",
    "spo2Daily",  # SpO2 Average recorded during sleep (officially documented)
]
API_BASE_URL: Final = "https://api.ouraring.com/v2/usercollection"

# Update interval
DEFAULT_UPDATE_INTERVAL: Final = 5  # minutes
MIN_UPDATE_INTERVAL: Final = 1  # minimum 1 minute to respect API rate limits
MAX_UPDATE_INTERVAL: Final = 60  # maximum 1 hour

# Historical data loading
DEFAULT_HISTORICAL_DAYS: Final = 14  # Fetch 14 days by default (safe for new users)
MIN_HISTORICAL_DAYS: Final = 1  # Minimum 1 day
MAX_HISTORICAL_DAYS: Final = 90  # Maximum 90 days (Oura API limit)

# Sensor types
SENSOR_TYPES: Final = {
    # Sleep sensors
    "sleep_score": {"name": "Sleep Score", "icon": "mdi:sleep", "unit": None, "device_class": None, "state_class": "measurement"},
    "total_sleep_duration": {"name": "Total Sleep Duration", "icon": "mdi:clock-outline", "unit": "h", "device_class": "duration", "state_class": "measurement"},
    "deep_sleep_duration": {"name": "Deep Sleep Duration", "icon": "mdi:sleep", "unit": "h", "device_class": "duration", "state_class": "measurement"},
    "rem_sleep_duration": {"name": "REM Sleep Duration", "icon": "mdi:sleep", "unit": "h", "device_class": "duration", "state_class": "measurement"},
    "light_sleep_duration": {"name": "Light Sleep Duration", "icon": "mdi:sleep", "unit": "h", "device_class": "duration", "state_class": "measurement"},
    "awake_time": {"name": "Awake Time", "icon": "mdi:eye", "unit": "h", "device_class": "duration", "state_class": "measurement"},
    "sleep_efficiency": {"name": "Sleep Efficiency", "icon": "mdi:percent", "unit": "%", "device_class": None, "state_class": "measurement"},
    "restfulness": {"name": "Restfulness", "icon": "mdi:bed", "unit": "%", "device_class": None, "state_class": "measurement"},
    "sleep_latency": {"name": "Sleep Latency", "icon": "mdi:timer", "unit": "min", "device_class": "duration", "state_class": "measurement"},
    "sleep_timing": {"name": "Sleep Timing", "icon": "mdi:clock-check", "unit": None, "device_class": None, "state_class": "measurement"},
    "deep_sleep_percentage": {"name": "Deep Sleep Percentage", "icon": "mdi:percent", "unit": "%", "device_class": None, "state_class": "measurement"},
    "rem_sleep_percentage": {"name": "REM Sleep Percentage", "icon": "mdi:percent", "unit": "%", "device_class": None, "state_class": "measurement"},
    "time_in_bed": {"name": "Time in Bed", "icon": "mdi:bed-clock", "unit": "h", "device_class": "duration", "state_class": "measurement"},
    
    # Readiness sensors
    "readiness_score": {"name": "Readiness Score", "icon": "mdi:heart-pulse", "unit": None, "device_class": None, "state_class": "measurement"},
    "temperature_deviation": {"name": "Temperature Deviation", "icon": "mdi:thermometer", "unit": "°C", "device_class": "temperature", "state_class": "measurement"},
    "resting_heart_rate": {"name": "Resting Heart Rate Score", "icon": "mdi:heart", "unit": None, "device_class": None, "state_class": "measurement"},
    "hrv_balance": {"name": "HRV Balance Score", "icon": "mdi:heart-pulse", "unit": None, "device_class": None, "state_class": "measurement"},
    
    # Activity sensors
    "activity_score": {"name": "Activity Score", "icon": "mdi:run", "unit": None, "device_class": None, "state_class": "measurement"},
    "steps": {"name": "Steps", "icon": "mdi:walk", "unit": "steps", "device_class": None, "state_class": "measurement"},
    "active_calories": {"name": "Active Calories", "icon": "mdi:fire", "unit": "kcal", "device_class": None, "state_class": "measurement"},
    "total_calories": {"name": "Total Calories", "icon": "mdi:fire", "unit": "kcal", "device_class": None, "state_class": "measurement"},
    "target_calories": {"name": "Target Calories", "icon": "mdi:bullseye", "unit": "kcal", "device_class": None, "state_class": "measurement"},
    "met_min_high": {"name": "High Activity Time", "icon": "mdi:run-fast", "unit": "min", "device_class": "duration", "state_class": "measurement"},
    "met_min_medium": {"name": "Medium Activity Time", "icon": "mdi:run", "unit": "min", "device_class": "duration", "state_class": "measurement"},
    "met_min_low": {"name": "Low Activity Time", "icon": "mdi:walk", "unit": "min", "device_class": "duration", "state_class": "measurement"},
    
    # Heart Rate sensors (from heartrate endpoint - more granular data)
    "current_heart_rate": {"name": "Current Heart Rate", "icon": "mdi:heart-pulse", "unit": "bpm", "device_class": None, "state_class": "measurement"},
    "average_heart_rate": {"name": "Average Heart Rate", "icon": "mdi:heart", "unit": "bpm", "device_class": None, "state_class": "measurement"},
    "min_heart_rate": {"name": "Minimum Heart Rate", "icon": "mdi:heart-minus", "unit": "bpm", "device_class": None, "state_class": "measurement"},
    "max_heart_rate": {"name": "Maximum Heart Rate", "icon": "mdi:heart-plus", "unit": "bpm", "device_class": None, "state_class": "measurement"},
    
    # HRV sensors (from detailed sleep endpoint)
    "average_sleep_hrv": {"name": "Average Sleep HRV", "icon": "mdi:heart-pulse", "unit": "ms", "device_class": None, "state_class": "measurement"},
    
    # Stress sensors
    "stress_high_duration": {"name": "Stress High Duration", "icon": "mdi:stress", "unit": "min", "device_class": "duration", "state_class": "measurement"},
    "recovery_high_duration": {"name": "Recovery High Duration", "icon": "mdi:lung", "unit": "min", "device_class": "duration", "state_class": "measurement"},
    "stress_day_summary": {"name": "Stress Day Summary", "icon": "mdi:stress", "unit": None, "device_class": None, "state_class": None},
    
    # Resilience sensors
    "resilience_level": {"name": "Resilience Level", "icon": "mdi:shield", "unit": None, "device_class": None, "state_class": None},
    "sleep_recovery_score": {"name": "Sleep Recovery Score", "icon": "mdi:bed-clock", "unit": None, "device_class": None, "state_class": "measurement"},
    "daytime_recovery_score": {"name": "Daytime Recovery Score", "icon": "mdi:sun-clock", "unit": None, "device_class": None, "state_class": "measurement"},
    "stress_resilience_score": {"name": "Stress Resilience Score", "icon": "mdi:shield-account", "unit": None, "device_class": None, "state_class": "measurement"},
    
    # SpO2 sensors (Gen3 and Oura Ring 4 only)
    "spo2_average": {"name": "SpO2 Average", "icon": "mdi:lung", "unit": "%", "device_class": None, "state_class": "measurement"},
    "breathing_disturbance_index": {"name": "Breathing Disturbance Index", "icon": "mdi:lung", "unit": None, "device_class": None, "state_class": "measurement"},
    
    # Fitness sensors
    "vo2_max": {"name": "VO2 Max", "icon": "mdi:heart-rate-monitor", "unit": "ml/kg/min", "device_class": None, "state_class": "measurement"},
    "cardiovascular_age": {"name": "Cardiovascular Age", "icon": "mdi:heart-rate-monitor", "unit": "years", "device_class": None, "state_class": "measurement"},
    
    # Sleep optimization sensors
    "optimal_bedtime_start": {"name": "Optimal Bedtime Start", "icon": "mdi:bed-clock", "unit": None, "device_class": "timestamp", "state_class": None},
    "optimal_bedtime_end": {"name": "Optimal Bedtime End", "icon": "mdi:bed-clock", "unit": None, "device_class": "timestamp", "state_class": None},
}
