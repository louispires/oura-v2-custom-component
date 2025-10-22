"""Sensor platform for Oura Ring integration."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN, SENSOR_TYPES
from .coordinator import OuraDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Oura Ring sensors."""
    coordinator: OuraDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        OuraSensor(coordinator, sensor_type, sensor_info)
        for sensor_type, sensor_info in SENSOR_TYPES.items()
    ]

    async_add_entities(entities)


class OuraSensor(CoordinatorEntity[OuraDataUpdateCoordinator], SensorEntity):
    """Representation of an Oura Ring sensor."""

    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        coordinator: OuraDataUpdateCoordinator,
        sensor_type: str,
        sensor_info: dict,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._attr_name = f"Oura {sensor_info['name']}"
        self._attr_unique_id = f"oura_{sensor_type}"
        self._attr_icon = sensor_info["icon"]
        self._attr_native_unit_of_measurement = sensor_info.get("unit")
        self._attr_device_class = sensor_info.get("device_class")
        self._attr_state_class = sensor_info.get("state_class")

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._sensor_type)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success
            and self._sensor_type in self.coordinator.data
            and self.coordinator.data[self._sensor_type] is not None
        )
