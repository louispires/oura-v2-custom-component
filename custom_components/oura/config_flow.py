"""Config flow for Oura Ring integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant import config_entries
from homeassistant.helpers import config_entry_oauth2_flow
from homeassistant.data_entry_flow import FlowResult
import voluptuous as vol

from .const import (
    DOMAIN,
    OAUTH2_SCOPES,
    CONF_UPDATE_INTERVAL,
    CONF_HISTORICAL_DAYS,
    DEFAULT_UPDATE_INTERVAL,
    DEFAULT_HISTORICAL_DAYS,
    MIN_UPDATE_INTERVAL,
    MAX_UPDATE_INTERVAL,
    MIN_HISTORICAL_DAYS,
    MAX_HISTORICAL_DAYS,
)

_LOGGER = logging.getLogger(__name__)


class OuraFlowHandler(
    config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN
):
    """Handle a config flow for Oura Ring."""

    DOMAIN = DOMAIN
    VERSION = 1

    @property
    def logger(self) -> logging.Logger:
        """Return logger."""
        return _LOGGER
    
    @property
    def extra_authorize_data(self) -> dict[str, Any]:
        """Extra data that needs to be appended to the authorize url."""
        return {
            "scope": " ".join(OAUTH2_SCOPES)
        }

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        return await super().async_step_user(user_input)

    async def async_oauth_create_entry(self, data: dict[str, Any]) -> config_entries.FlowResult:
        """Create an entry for Oura Ring."""
        _LOGGER.info("Successfully authenticated")
        _LOGGER.debug("OAuth data keys: %s", list(data.keys()))
        return self.async_create_entry(title="Oura Ring", data=data)

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> OuraOptionsFlowHandler:
        """Get the options flow for this handler."""
        return OuraOptionsFlowHandler()


class OuraOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Oura Ring options."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_UPDATE_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
                        ),
                    ): vol.All(
                        vol.Coerce(int),
                        vol.Range(min=MIN_UPDATE_INTERVAL, max=MAX_UPDATE_INTERVAL),
                    ),
                    vol.Optional(
                        CONF_HISTORICAL_DAYS,
                        default=self.config_entry.options.get(
                            CONF_HISTORICAL_DAYS, DEFAULT_HISTORICAL_DAYS
                        ),
                    ): vol.All(
                        vol.Coerce(int),
                        vol.Range(min=MIN_HISTORICAL_DAYS, max=MAX_HISTORICAL_DAYS),
                    ),
                }
            ),
        )
