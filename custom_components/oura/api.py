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

    async def async_get_data(self) -> dict[str, Any]:
        """Get data from Oura API."""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=1)
        
        sleep_data, readiness_data, activity_data, heartrate_data, sleep_detail_data = await asyncio.gather(
            self._async_get_sleep(start_date, end_date),
            self._async_get_readiness(start_date, end_date),
            self._async_get_activity(start_date, end_date),
            self._async_get_heartrate(start_date, end_date),
            self._async_get_sleep_detail(start_date, end_date),
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

        return {
            "sleep": sleep_data if not isinstance(sleep_data, Exception) else {},
            "readiness": readiness_data if not isinstance(readiness_data, Exception) else {},
            "activity": activity_data if not isinstance(activity_data, Exception) else {},
            "heartrate": heartrate_data if not isinstance(heartrate_data, Exception) else {},
            "sleep_detail": sleep_detail_data if not isinstance(sleep_detail_data, Exception) else {},
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
        """Get heart rate data."""
        url = f"{API_BASE_URL}/heartrate"
        params = {
            "start_datetime": f"{start_date.isoformat()}T00:00:00",
            "end_datetime": f"{end_date.isoformat()}T23:59:59",
        }
        return await self._async_get(url, params)

    async def _async_get_sleep_detail(self, start_date: datetime.date, end_date: datetime.date) -> dict[str, Any]:
        """Get detailed sleep data including HRV."""
        url = f"{API_BASE_URL}/sleep"
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
