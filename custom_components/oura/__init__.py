"""The Oura Ring integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_oauth2_flow, config_validation as cv

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

# Config entry only (no YAML configuration)
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Oura Ring from a config entry."""
    _LOGGER.debug("Setting up Oura Ring entry. Entry data keys: %s", list(entry.data.keys()))
    
    implementation = (
        await config_entry_oauth2_flow.async_get_config_entry_implementation(
            hass, entry
        )
    )

    session = config_entry_oauth2_flow.OAuth2Session(hass, entry, implementation)
    
    # Log session state for debugging
    _LOGGER.debug("OAuth2Session created. Valid token: %s", session.valid_token)
    
    # Pass the entry to the API client so it can access the token directly
    api_client = OuraApiClient(hass, session, entry)
    
    # Get update interval from options, or use default
    update_interval = entry.options.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
    coordinator = OuraDataUpdateCoordinator(hass, api_client, entry, update_interval)

    # Check if this is the first setup (no historical data loaded yet)
    # We'll use a flag stored in hass.data to track this
    hass.data.setdefault(DOMAIN, {})
    is_first_setup = entry.entry_id not in hass.data[DOMAIN]
    
    if is_first_setup:
        # Get historical days from options, or use default
        historical_days = entry.options.get(CONF_HISTORICAL_DAYS, DEFAULT_HISTORICAL_DAYS)
        
        _LOGGER.info("Loading %d days of historical data...", historical_days)
        
        # Load historical data before first refresh
        try:
            await coordinator.async_load_historical_data(historical_days)
        except Exception as err:
            _LOGGER.error("Failed to load historical data: %s", err)
            # Continue anyway - regular updates will still work
    
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
