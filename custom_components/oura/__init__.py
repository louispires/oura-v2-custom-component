"""The Oura Ring integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_oauth2_flow

from .api import OuraApiClient
from .const import (
    DOMAIN,
    CONF_UPDATE_INTERVAL,
    CONF_HISTORICAL_DAYS,
    DEFAULT_UPDATE_INTERVAL,
    DEFAULT_HISTORICAL_DAYS,
)
from .coordinator import OuraDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Oura Ring component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Oura Ring from a config entry."""
    _LOGGER.debug("Setting up Oura Ring config entry: %s", entry.entry_id)
    _LOGGER.debug("Entry data keys: %s", list(entry.data.keys()))
    
    # Check what's in the token data
    if 'token' in entry.data:
        token_data = entry.data.get('token')
        _LOGGER.debug("Token data type: %s", type(token_data))
        if isinstance(token_data, dict):
            _LOGGER.debug("Token data keys: %s", list(token_data.keys()))
    
    implementation = (
        await config_entry_oauth2_flow.async_get_config_entry_implementation(
            hass, entry
        )
    )

    session = config_entry_oauth2_flow.OAuth2Session(hass, entry, implementation)
    
    # Pass the entry to the API client so it can access the token directly
    api_client = OuraApiClient(hass, session, entry)
    
    # Get update interval from options, or use default
    update_interval = entry.options.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
    coordinator = OuraDataUpdateCoordinator(hass, api_client, update_interval)

    # Check if this is the first setup (no historical data loaded yet)
    # We'll use a flag stored in hass.data to track this
    hass.data.setdefault(DOMAIN, {})
    is_first_setup = entry.entry_id not in hass.data[DOMAIN]
    
    _LOGGER.info("Integration setup - Entry ID: %s, First setup: %s", entry.entry_id, is_first_setup)
    
    if is_first_setup:
        # Get historical days from options, or use default
        historical_days = entry.options.get(CONF_HISTORICAL_DAYS, DEFAULT_HISTORICAL_DAYS)
        
        _LOGGER.info("First setup detected - will load %d days of historical data", historical_days)
        
        # Load historical data before first refresh
        try:
            await coordinator.async_load_historical_data(historical_days)
            _LOGGER.info("Historical data load completed successfully")
        except Exception as err:
            _LOGGER.error("Failed to load historical data: %s", err, exc_info=True)
            # Continue anyway - regular updates will still work
    else:
        _LOGGER.info("Not first setup - skipping historical data load")
    
    # Do the first refresh (or subsequent refreshes)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Register update listener for options changes
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry when options change."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
