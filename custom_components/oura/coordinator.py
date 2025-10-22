"""DataUpdateCoordinator for Oura Ring."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import OuraApiClient
from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL, CONF_UPDATE_INTERVAL

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

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via API."""
        try:
            data = await self.api_client.async_get_data()
            return self._process_data(data)
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    def _process_data(self, data: dict[str, Any]) -> dict[str, Any]:
        """Process the raw API data into sensor values."""
        processed = {}
        
        # Process sleep data
        if sleep_data := data.get("sleep", {}).get("data"):
            if sleep_data and len(sleep_data) > 0:
                latest_sleep = sleep_data[-1]
                if contributors := latest_sleep.get("contributors"):
                    processed["sleep_score"] = latest_sleep.get("score")
                    processed["total_sleep_duration"] = contributors.get("total_sleep_duration", 0) / 3600
                    processed["deep_sleep_duration"] = contributors.get("deep_sleep", 0) / 3600
                    processed["rem_sleep_duration"] = contributors.get("rem_sleep", 0) / 3600
                    processed["light_sleep_duration"] = contributors.get("light_sleep", 0) / 3600
                    processed["awake_time"] = latest_sleep.get("time_in_bed", 0) / 3600 - processed.get("total_sleep_duration", 0)
                    processed["sleep_efficiency"] = contributors.get("efficiency")
                    processed["restfulness"] = contributors.get("restfulness")
                    processed["sleep_latency"] = contributors.get("latency", 0) / 60
                    processed["sleep_timing"] = contributors.get("timing")
        
        # Process readiness data
        if readiness_data := data.get("readiness", {}).get("data"):
            if readiness_data and len(readiness_data) > 0:
                latest_readiness = readiness_data[-1]
                if contributors := latest_readiness.get("contributors"):
                    processed["readiness_score"] = latest_readiness.get("score")
                    processed["temperature_deviation"] = latest_readiness.get("temperature_deviation")
                    processed["resting_heart_rate"] = contributors.get("resting_heart_rate")
                    processed["hrv_balance"] = contributors.get("hrv_balance")
        
        # Process activity data
        if activity_data := data.get("activity", {}).get("data"):
            if activity_data and len(activity_data) > 0:
                latest_activity = activity_data[-1]
                if contributors := latest_activity.get("contributors"):
                    processed["activity_score"] = latest_activity.get("score")
                    processed["steps"] = latest_activity.get("steps")
                    processed["active_calories"] = latest_activity.get("active_calories")
                    processed["total_calories"] = latest_activity.get("total_calories")
                    processed["target_calories"] = latest_activity.get("target_calories")
                    processed["met_min_high"] = contributors.get("meet_daily_targets")
                    processed["met_min_medium"] = contributors.get("move_every_hour")
                    processed["met_min_low"] = contributors.get("recovery_time")
        
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
        
        return processed
