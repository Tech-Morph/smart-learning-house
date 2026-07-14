"""Switch entity: enable/disable the smart temperature automation."""
from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, DAIKIN_DOMAIN
from .smart_controller import SmartTemperatureController


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    controller: SmartTemperatureController = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([SmartTempSwitch(controller, entry)])


class SmartTempSwitch(SwitchEntity):
    _attr_has_entity_name = True
    _attr_name = "Smart Temperature"
    _attr_icon = "mdi:home-thermometer"

    def __init__(self, controller: SmartTemperatureController, entry: ConfigEntry) -> None:
        self._controller = controller
        self._attr_unique_id = f"{DOMAIN}_switch_{entry.data['device_id']}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.data['device_id'])},
            name=f"Daikin Smart Temp — {controller.coordinator.device_name}",
            manufacturer="Tech-Morph",
            model="Smart Temperature Controller",
            via_device=(DAIKIN_DOMAIN, entry.data['device_id']),
        )

    @property
    def is_on(self) -> bool:
        return self._controller._enabled

    async def async_turn_on(self, **kwargs) -> None:
        self._controller.set_enabled(True)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        self._controller.set_enabled(False)
        self.async_write_ha_state()
