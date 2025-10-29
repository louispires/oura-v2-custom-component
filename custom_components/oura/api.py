"""API client for Oura Ring."""
from __future__ import annotations

import asyncio
from datetime import datetime, timedelta
import logging
from typing import Any

from aiohttp import ClientSession
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.config_entry_oauth2_flow import OAuth2Session
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import API_BASE_URL

_LOGGER = logging.getLogger(__name__)


class OuraApiClient:
    """Oura API client."""

    def __init__(self, hass: HomeAssistant, session: OAuth2Session, entry: ConfigEntry) -> None:
        """Initialize the API client."""
        self.hass = hass
        self.session = session
        self.entry = entry
        self._client_session: ClientSession | None = None

    @property
    def client_session(self) -> ClientSession:
        """Get aiohttp client session."""
        if self._client_session is None:
            self._client_session = async_get_clientsession(self.hass)
        return self._client_session

    async def async_get_data(self, days_back: int = 1) -> dict[str, Any]:
        """Get data from Oura API.
        
        Args:
            days_back: Number of days of historical data to fetch (default: 1)
        """
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days_back)
        
        _LOGGER.debug("Fetching Oura data from %s to %s (%d days)", start_date, end_date, days_back)
        
        sleep_data, readiness_data, activity_data, heartrate_data, sleep_detail_data, stress_data, resilience_data, spo2_data, vo2_max_data, cardiovascular_age_data, sleep_time_data = await asyncio.gather(
            self._async_get_sleep(start_date, end_date),
            self._async_get_readiness(start_date, end_date),
            self._async_get_activity(start_date, end_date),
            self._async_get_heartrate(start_date, end_date),
            self._async_get_sleep_detail(start_date, end_date),
            self._async_get_stress(start_date, end_date),
            self._async_get_resilience(start_date, end_date),
            self._async_get_spo2(start_date, end_date),
            self._async_get_vo2_max(start_date, end_date),
            self._async_get_cardiovascular_age(start_date, end_date),
            self._async_get_sleep_time(start_date, end_date),
            return_exceptions=True,
        )

        # Log any exceptions that occurred
        if isinstance(sleep_data, Exception):
            _LOGGER.error("Error fetching sleep data: %s", sleep_data)
        if isinstance(readiness_data, Exception):
            _LOGGER.error("Error fetching readiness data: %s", readiness_data)
        if isinstance(activity_data, Exception):
            _LOGGER.error("Error fetching activity data: %s", activity_data)
        if isinstance(heartrate_data, Exception):
            _LOGGER.error("Error fetching heart rate data: %s", heartrate_data)
        if isinstance(sleep_detail_data, Exception):
            _LOGGER.error("Error fetching detailed sleep data: %s", sleep_detail_data)
        if isinstance(stress_data, Exception):
            _LOGGER.error("Error fetching stress data: %s", stress_data)
        if isinstance(resilience_data, Exception):
            _LOGGER.error("Error fetching resilience data: %s", resilience_data)
        if isinstance(spo2_data, Exception):
            _LOGGER.error("Error fetching SpO2 data: %s", spo2_data)
        if isinstance(vo2_max_data, Exception):
            _LOGGER.error("Error fetching VO2 Max data: %s", vo2_max_data)
        if isinstance(cardiovascular_age_data, Exception):
            _LOGGER.error("Error fetching cardiovascular age data: %s", cardiovascular_age_data)
        if isinstance(sleep_time_data, Exception):
            _LOGGER.error("Error fetching sleep time data: %s", sleep_time_data)

        return {
            "sleep": sleep_data if not isinstance(sleep_data, Exception) else {},
            "readiness": readiness_data if not isinstance(readiness_data, Exception) else {},
            "activity": activity_data if not isinstance(activity_data, Exception) else {},
            "heartrate": heartrate_data if not isinstance(heartrate_data, Exception) else {},
            "sleep_detail": sleep_detail_data if not isinstance(sleep_detail_data, Exception) else {},
            "stress": stress_data if not isinstance(stress_data, Exception) else {},
            "resilience": resilience_data if not isinstance(resilience_data, Exception) else {},
            "spo2": spo2_data if not isinstance(spo2_data, Exception) else {},
            "vo2_max": vo2_max_data if not isinstance(vo2_max_data, Exception) else {},
            "cardiovascular_age": cardiovascular_age_data if not isinstance(cardiovascular_age_data, Exception) else {},
            "sleep_time": sleep_time_data if not isinstance(sleep_time_data, Exception) else {},
        }

    async def _async_get_sleep(self, start_date: datetime.date, end_date: datetime.date) -> dict[str, Any]:
        """Get sleep data."""
        url = f"{API_BASE_URL}/daily_sleep"
        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }
        return await self._async_get(url, params)

    async def _async_get_readiness(self, start_date: datetime.date, end_date: datetime.date) -> dict[str, Any]:
        """Get readiness data."""
        url = f"{API_BASE_URL}/daily_readiness"
        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }
        return await self._async_get(url, params)

    async def _async_get_activity(self, start_date: datetime.date, end_date: datetime.date) -> dict[str, Any]:
        """Get activity data."""
        url = f"{API_BASE_URL}/daily_activity"
        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }
        return await self._async_get(url, params)

    async def _async_get_heartrate(self, start_date: datetime.date, end_date: datetime.date) -> dict[str, Any]:
        """Get heart rate data.
        
        Note: The heartrate endpoint has a maximum range of 7 days.
        For historical data requests, we'll batch the requests.
        """
        url = f"{API_BASE_URL}/heartrate"
        
        # Calculate the number of days in the range
        days_range = (end_date - start_date).days
        
        # If range is > 7 days, batch the requests
        if days_range > 7:
            _LOGGER.debug("Heart rate range is %d days, batching into 7-day chunks", days_range)
            all_data = []
            current_start = start_date
            
            while current_start < end_date:
                current_end = min(current_start + timedelta(days=7), end_date)
                params = {
                    "start_datetime": f"{current_start.isoformat()}T00:00:00",
                    "end_datetime": f"{current_end.isoformat()}T23:59:59",
                }
                
                try:
                    batch_data = await self._async_get(url, params)
                    if batch_data and "data" in batch_data:
                        all_data.extend(batch_data["data"])
                except Exception as err:
                    _LOGGER.warning(
                        "Failed to fetch heart rate data for %s to %s: %s",
                        current_start, current_end, err
                    )
                
                current_start = current_end + timedelta(days=1)
            
            return {"data": all_data}
        else:
            # Range is 7 days or less, single request
            params = {
                "start_datetime": f"{start_date.isoformat()}T00:00:00",
                "end_datetime": f"{end_date.isoformat()}T23:59:59",
            }
            
            try:
                return await self._async_get(url, params)
            except Exception as err:
                _LOGGER.error("Heart rate endpoint failed: %s", err)
                # Return empty data instead of failing completely
                return {"data": []}

    async def _async_get_sleep_detail(self, start_date: datetime.date, end_date: datetime.date) -> dict[str, Any]:
        """Get detailed sleep data including HRV."""
        url = f"{API_BASE_URL}/sleep"
        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }
        return await self._async_get(url, params)

    async def _async_get_stress(self, start_date: datetime.date, end_date: datetime.date) -> dict[str, Any]:
        """Get daily stress data."""
        url = f"{API_BASE_URL}/daily_stress"
        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }
        return await self._async_get(url, params)

    async def _async_get_resilience(self, start_date: datetime.date, end_date: datetime.date) -> dict[str, Any]:
        """Get daily resilience data."""
        url = f"{API_BASE_URL}/daily_resilience"
        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }
        return await self._async_get(url, params)

    async def _async_get_spo2(self, start_date: datetime.date, end_date: datetime.date) -> dict[str, Any]:
        """Get daily SpO2 (blood oxygen) data. Available for Gen3 and Oura Ring 4."""
        url = f"{API_BASE_URL}/daily_spo2"
        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }
        return await self._async_get(url, params)

    async def _async_get_vo2_max(self, start_date: datetime.date, end_date: datetime.date) -> dict[str, Any]:
        """Get VO2 Max fitness data."""
        url = f"{API_BASE_URL}/v2/usercollection/vO2_max"
        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }
        return await self._async_get(url, params)

    async def _async_get_cardiovascular_age(self, start_date: datetime.date, end_date: datetime.date) -> dict[str, Any]:
        """Get daily cardiovascular age data."""
        url = f"{API_BASE_URL}/daily_cardiovascular_age"
        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }
        return await self._async_get(url, params)

    async def _async_get_sleep_time(self, start_date: datetime.date, end_date: datetime.date) -> dict[str, Any]:
        """Get optimal sleep time recommendations."""
        url = f"{API_BASE_URL}/sleep_time"
        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }
        return await self._async_get(url, params)

    async def _async_get(self, url: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make GET request to Oura API."""
        # Try to get token from async_ensure_token_valid first
        try:
            token = await self.session.async_ensure_token_valid()
        except Exception as err:
            _LOGGER.error("Error ensuring token is valid: %s", err, exc_info=True)
            token = None
        
        # If that returns None, get it directly from the config entry
        if token is None:
            _LOGGER.debug("async_ensure_token_valid() returned None, getting token from entry.data")
            token = self.entry.data.get("token")
            
        if token is None:
            _LOGGER.error("Token is None - both async_ensure_token_valid() and entry.data['token'] returned None")
            raise ValueError("OAuth2 token is None")
        
        if not isinstance(token, dict):
            _LOGGER.error("Token is not a dict, it's a %s: %s", type(token), token)
            raise ValueError(f"OAuth2 token is not a dict: {type(token)}")
        
        if 'access_token' not in token:
            _LOGGER.error("Token dict missing 'access_token' key. Token keys: %s", list(token.keys()))
            raise ValueError("OAuth2 token missing 'access_token'")
        
        headers = {
            "Authorization": f"Bearer {token['access_token']}",
        }
        
        _LOGGER.debug("Making request to %s with params %s", url, params)
        
        try:
            async with self.client_session.get(url, headers=headers, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                _LOGGER.debug("Received response from %s: %s items", url, len(data.get('data', [])) if isinstance(data, dict) else 'unknown')
                return data
        except Exception as err:
            _LOGGER.error("Error fetching data from %s: %s", url, err)
            raise
