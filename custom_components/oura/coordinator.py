"""DataUpdateCoordinator for Oura Ring."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import OuraApiClient
from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL
from .statistics import async_import_statistics

_LOGGER = logging.getLogger(__name__)


class OuraDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching Oura Ring data."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_client: OuraApiClient,
        update_interval_minutes: int = DEFAULT_UPDATE_INTERVAL,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=update_interval_minutes),
        )
        self.api_client = api_client
        self.historical_data_loaded = False

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via API."""
        try:
            # For regular updates, only fetch 1 day of data
            data = await self.api_client.async_get_data(days_back=1)
            return self._process_data(data)
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
    
    async def async_load_historical_data(self, days: int) -> None:
        """Load historical data on first setup.
        
        Args:
            days: Number of days of historical data to fetch
        """
        try:
            _LOGGER.info("Fetching %d days of historical Oura data...", days)
            historical_data = await self.api_client.async_get_data(days_back=days)
            
            _LOGGER.debug("Historical data fetched. Keys: %s", list(historical_data.keys()))
            
            # Import historical data as long-term statistics
            _LOGGER.info("Importing historical data as long-term statistics...")
            try:
                await async_import_statistics(self.hass, historical_data)
                _LOGGER.info("Statistics import completed successfully")
            except Exception as stats_err:
                _LOGGER.error("Failed to import statistics: %s", stats_err, exc_info=True)
                raise
            
            # Process and store the LATEST day's data for current sensor states
            processed_data = self._process_data(historical_data)
            
            _LOGGER.debug("Processed current data. Keys: %s", list(processed_data.keys()))
            
            # Update the coordinator's data with current information
            self.data = processed_data
            self.historical_data_loaded = True
            
            _LOGGER.info("Successfully loaded %d days of historical data and %d current metrics", 
                        days, len(processed_data))
        except Exception as err:
            _LOGGER.error("Failed to fetch historical data: %s", err, exc_info=True)
            _LOGGER.warning("Will continue with daily updates only")
            raise

    def _process_data(self, data: dict[str, Any]) -> dict[str, Any]:
        """Process the raw API data into sensor values."""
        processed = {}
        
        # Process sleep data (daily_sleep endpoint has scores, sleep_detail has actual durations)
        if sleep_data := data.get("sleep", {}).get("data"):
            if sleep_data and len(sleep_data) > 0:
                latest_sleep = sleep_data[-1]
                if contributors := latest_sleep.get("contributors"):
                    processed["sleep_score"] = latest_sleep.get("score")
                    # These are contribution scores (1-100), not durations
                    processed["sleep_efficiency"] = contributors.get("efficiency")
                    processed["restfulness"] = contributors.get("restfulness")
                    processed["sleep_timing"] = contributors.get("timing")
        
        # Process detailed sleep data for actual sleep durations and HRV
        if sleep_detail_data := data.get("sleep_detail", {}).get("data"):
            if sleep_detail_data and len(sleep_detail_data) > 0:
                latest_sleep_detail = sleep_detail_data[-1]
                # These are actual durations in seconds
                total_sleep_seconds = latest_sleep_detail.get("total_sleep_duration")
                deep_sleep_seconds = latest_sleep_detail.get("deep_sleep_duration")
                rem_sleep_seconds = latest_sleep_detail.get("rem_sleep_duration")
                light_sleep_seconds = latest_sleep_detail.get("light_sleep_duration")
                
                if total_sleep_seconds:
                    processed["total_sleep_duration"] = total_sleep_seconds / 3600  # Convert to hours
                if deep_sleep_seconds:
                    processed["deep_sleep_duration"] = deep_sleep_seconds / 3600
                if rem_sleep_seconds:
                    processed["rem_sleep_duration"] = rem_sleep_seconds / 3600
                if light_sleep_seconds:
                    processed["light_sleep_duration"] = light_sleep_seconds / 3600
                if awake := latest_sleep_detail.get("awake_time"):
                    processed["awake_time"] = awake / 3600
                if latency := latest_sleep_detail.get("latency"):
                    processed["sleep_latency"] = latency / 60  # Convert to minutes
                if time_in_bed := latest_sleep_detail.get("time_in_bed"):
                    processed["time_in_bed"] = time_in_bed / 3600  # Convert to hours
                
                # Calculate sleep stage percentages
                if total_sleep_seconds and total_sleep_seconds > 0:
                    if deep_sleep_seconds is not None:
                        processed["deep_sleep_percentage"] = round((deep_sleep_seconds / total_sleep_seconds) * 100, 1)
                    if rem_sleep_seconds is not None:
                        processed["rem_sleep_percentage"] = round((rem_sleep_seconds / total_sleep_seconds) * 100, 1)
                
                # Get average HRV from sleep period
                if average_hrv := latest_sleep_detail.get("average_hrv"):
                    processed["average_sleep_hrv"] = average_hrv
        
        # Process readiness data (contributors are scores 1-100, not actual values)
        if readiness_data := data.get("readiness", {}).get("data"):
            if readiness_data and len(readiness_data) > 0:
                latest_readiness = readiness_data[-1]
                processed["readiness_score"] = latest_readiness.get("score")
                # temperature_deviation is actual temperature in Celsius
                processed["temperature_deviation"] = latest_readiness.get("temperature_deviation")
                # These are contribution scores (1-100), not actual BPM or HRV values
                if contributors := latest_readiness.get("contributors"):
                    _LOGGER.debug("Readiness contributors: %s", contributors)
                    rhr = contributors.get("resting_heart_rate")
                    hrv = contributors.get("hrv_balance")
                    _LOGGER.debug("Resting HR: %s, HRV Balance: %s", rhr, hrv)
                    processed["resting_heart_rate"] = rhr
                    processed["hrv_balance"] = hrv
        
        # Process activity data
        if activity_data := data.get("activity", {}).get("data"):
            if activity_data and len(activity_data) > 0:
                latest_activity = activity_data[-1]
                processed["activity_score"] = latest_activity.get("score")
                processed["steps"] = latest_activity.get("steps")
                processed["active_calories"] = latest_activity.get("active_calories")
                processed["total_calories"] = latest_activity.get("total_calories")
                processed["target_calories"] = latest_activity.get("target_calories")
                # MET minutes are directly on the activity object, not in contributors
                processed["met_min_high"] = latest_activity.get("high_activity_met_minutes")
                processed["met_min_medium"] = latest_activity.get("medium_activity_met_minutes")
                processed["met_min_low"] = latest_activity.get("low_activity_met_minutes")
        
        # Process heart rate data
        if heartrate_data := data.get("heartrate", {}).get("data"):
            if heartrate_data and len(heartrate_data) > 0:
                # Get latest heart rate reading
                latest_hr = heartrate_data[-1]
                processed["current_heart_rate"] = latest_hr.get("bpm")
                processed["heart_rate_timestamp"] = latest_hr.get("timestamp")
                
                # Calculate average heart rate from recent readings
                recent_readings = [hr.get("bpm") for hr in heartrate_data[-10:] if hr.get("bpm")]
                if recent_readings:
                    processed["average_heart_rate"] = sum(recent_readings) / len(recent_readings)
                    processed["min_heart_rate"] = min(recent_readings)
                    processed["max_heart_rate"] = max(recent_readings)
        
        # Process stress data
        if stress_data := data.get("stress", {}).get("data"):
            if stress_data and len(stress_data) > 0:
                latest_stress = stress_data[-1]
                processed["stress_high_duration"] = latest_stress.get("stress_high_duration")
                processed["recovery_high_duration"] = latest_stress.get("recovery_high_duration")
                # stress_day_summary is an enum: good, bad, or unknown
                processed["stress_day_summary"] = latest_stress.get("day_summary")
        
        # Process resilience data
        if resilience_data := data.get("resilience", {}).get("data"):
            if resilience_data and len(resilience_data) > 0:
                latest_resilience = resilience_data[-1]
                # resilience_level is an enum: limited, adequate, solid, strong, exceptional
                processed["resilience_level"] = latest_resilience.get("level")
                processed["sleep_recovery_score"] = latest_resilience.get("sleep_recovery_score")
                processed["daytime_recovery_score"] = latest_resilience.get("daytime_recovery_score")
                if contributors := latest_resilience.get("contributors"):
                    processed["stress_resilience_score"] = contributors.get("activity_score")
        
        # Process SpO2 data (blood oxygen) - Available for Gen3 and Oura Ring 4
        if spo2_data := data.get("spo2", {}).get("data"):
            _LOGGER.debug("SpO2 data found: %s items", len(spo2_data))
            if spo2_data and len(spo2_data) > 0:
                latest_spo2 = spo2_data[-1]
                _LOGGER.debug("Latest SpO2 entry: %s", latest_spo2)
                # The API returns spo2_percentage as an object with an 'average' field
                if spo2_percentage := latest_spo2.get("spo2_percentage"):
                    processed["spo2_average"] = spo2_percentage.get("average")
                processed["breathing_disturbance_index"] = latest_spo2.get("breathing_disturbance_index")
                _LOGGER.debug("Processed SpO2 average: %s, BDI: %s", 
                             processed.get("spo2_average"), 
                             processed.get("breathing_disturbance_index"))
        
        # Process VO2 Max data
        if vo2_max_data := data.get("vo2_max", {}).get("data"):
            if vo2_max_data and len(vo2_max_data) > 0:
                latest_vo2 = vo2_max_data[-1]
                processed["vo2_max"] = latest_vo2.get("vo2_max")
        
        # Process cardiovascular age data
        if cardiovascular_age_data := data.get("cardiovascular_age", {}).get("data"):
            if cardiovascular_age_data and len(cardiovascular_age_data) > 0:
                latest_cv_age = cardiovascular_age_data[-1]
                processed["cardiovascular_age"] = latest_cv_age.get("age")
        
        # Process sleep time recommendations
        if sleep_time_data := data.get("sleep_time", {}).get("data"):
            if sleep_time_data and len(sleep_time_data) > 0:
                latest_sleep_time = sleep_time_data[-1]
                # These are time windows for optimal sleep, returned as ISO 8601 time strings
                processed["optimal_bedtime_start"] = latest_sleep_time.get("optimal_bedtime_start")
                processed["optimal_bedtime_end"] = latest_sleep_time.get("optimal_bedtime_end")
        
        return processed
