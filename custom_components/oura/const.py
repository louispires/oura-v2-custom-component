"""Constants for the Oura Ring integration."""
from datetime import timedelta
from typing import Final

DOMAIN: Final = "oura"
ATTRIBUTION: Final = "Data provided by Oura Ring"

# Configuration
CONF_UPDATE_INTERVAL: Final = "update_interval"

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
]
API_BASE_URL: Final = "https://api.ouraring.com/v2/usercollection"

# Update interval
DEFAULT_UPDATE_INTERVAL: Final = 5  # minutes
MIN_UPDATE_INTERVAL: Final = 1  # minimum 1 minute to respect API rate limits
MAX_UPDATE_INTERVAL: Final = 60  # maximum 1 hour

# Sensor types
SENSOR_TYPES: Final = {
    # Sleep sensors
    "sleep_score": {"name": "Sleep Score", "icon": "mdi:sleep", "unit": None, "device_class": None, "state_class": "measurement"},
    "total_sleep_duration": {"name": "Total Sleep Duration", "icon": "mdi:clock-outline", "unit": "h", "device_class": "duration", "state_class": "total_increasing"},
    "deep_sleep_duration": {"name": "Deep Sleep Duration", "icon": "mdi:sleep", "unit": "h", "device_class": "duration", "state_class": "total_increasing"},
    "rem_sleep_duration": {"name": "REM Sleep Duration", "icon": "mdi:sleep", "unit": "h", "device_class": "duration", "state_class": "total_increasing"},
    "light_sleep_duration": {"name": "Light Sleep Duration", "icon": "mdi:sleep", "unit": "h", "device_class": "duration", "state_class": "total_increasing"},
    "awake_time": {"name": "Awake Time", "icon": "mdi:eye", "unit": "h", "device_class": "duration", "state_class": "total_increasing"},
    "sleep_efficiency": {"name": "Sleep Efficiency", "icon": "mdi:percent", "unit": "%", "device_class": None, "state_class": "measurement"},
    "restfulness": {"name": "Restfulness", "icon": "mdi:bed", "unit": "%", "device_class": None, "state_class": "measurement"},
    "sleep_latency": {"name": "Sleep Latency", "icon": "mdi:timer", "unit": "min", "device_class": "duration", "state_class": "measurement"},
    "sleep_timing": {"name": "Sleep Timing", "icon": "mdi:clock-check", "unit": None, "device_class": None, "state_class": "measurement"},
    
    # Readiness sensors
    "readiness_score": {"name": "Readiness Score", "icon": "mdi:heart-pulse", "unit": None, "device_class": None, "state_class": "measurement"},
    "temperature_deviation": {"name": "Temperature Deviation", "icon": "mdi:thermometer", "unit": "°C", "device_class": "temperature", "state_class": "measurement"},
    "resting_heart_rate": {"name": "Resting Heart Rate", "icon": "mdi:heart", "unit": "bpm", "device_class": None, "state_class": "measurement"},
    "hrv_balance": {"name": "HRV Balance", "icon": "mdi:heart-pulse", "unit": None, "device_class": None, "state_class": "measurement"},
    
    # Activity sensors
    "activity_score": {"name": "Activity Score", "icon": "mdi:run", "unit": None, "device_class": None, "state_class": "measurement"},
    "steps": {"name": "Steps", "icon": "mdi:walk", "unit": "steps", "device_class": None, "state_class": "total_increasing"},
    "active_calories": {"name": "Active Calories", "icon": "mdi:fire", "unit": "kcal", "device_class": None, "state_class": "total_increasing"},
    "total_calories": {"name": "Total Calories", "icon": "mdi:fire", "unit": "kcal", "device_class": None, "state_class": "total_increasing"},
    "target_calories": {"name": "Target Calories", "icon": "mdi:bullseye", "unit": "kcal", "device_class": None, "state_class": "measurement"},
    "met_min_high": {"name": "High Activity Time", "icon": "mdi:run-fast", "unit": "min", "device_class": "duration", "state_class": "total_increasing"},
    "met_min_medium": {"name": "Medium Activity Time", "icon": "mdi:run", "unit": "min", "device_class": "duration", "state_class": "total_increasing"},
    "met_min_low": {"name": "Low Activity Time", "icon": "mdi:walk", "unit": "min", "device_class": "duration", "state_class": "total_increasing"},
    
    # Heart Rate sensors (from heartrate endpoint - more granular data)
    "current_heart_rate": {"name": "Current Heart Rate", "icon": "mdi:heart-pulse", "unit": "bpm", "device_class": None, "state_class": "measurement"},
    "average_heart_rate": {"name": "Average Heart Rate", "icon": "mdi:heart", "unit": "bpm", "device_class": None, "state_class": "measurement"},
    "min_heart_rate": {"name": "Minimum Heart Rate", "icon": "mdi:heart-minus", "unit": "bpm", "device_class": None, "state_class": "measurement"},
    "max_heart_rate": {"name": "Maximum Heart Rate", "icon": "mdi:heart-plus", "unit": "bpm", "device_class": None, "state_class": "measurement"},
}
