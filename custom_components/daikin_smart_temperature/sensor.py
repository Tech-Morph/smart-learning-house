"""Sensor entities: target temp and last commanded mode."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
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
    entities = [
        SmartTargetTempSensor(controller, entry),
        SmartLastModeSensor(controller, entry),
    ]
    # Register options-change callbacks so Lovelace updates immediately
    for entity in entities:
        controller.register_options_callback(entity.schedule_update)
    async_add_entities(entities)


class _SmartTempBase(SensorEntity):
    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, controller: SmartTemperatureController, entry: ConfigEntry) -> None:
        self._controller = controller
        self._entry = entry
        device_id = entry.data['device_id']
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=f"Daikin Smart Temp — {controller.coordinator.device_name}",
            manufacturer="Tech-Morph",
            model="Smart Temperature Controller",
            via_device=(DAIKIN_DOMAIN, device_id),
        )

    def schedule_update(self) -> None:
        """Called by controller when options change — pushes new state to HA."""
        self.schedule_update_ha_state()


class SmartTargetTempSensor(_SmartTempBase):
    _attr_name = "Smart Target Temperature"
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class  = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.FAHRENHEIT
    _attr_icon = "mdi:thermometer-check"

    def __init__(self, controller: SmartTemperatureController, entry: ConfigEntry) -> None:
        super().__init__(controller, entry)
        self._attr_unique_id = f"{DOMAIN}_target_temp_{entry.data['device_id']}"

    @property
    def native_value(self) -> float:
        return round(self._controller.current_target_f, 1)


class SmartLastModeSensor(_SmartTempBase):
    _attr_name = "Smart Last Mode"
    _attr_icon = "mdi:air-conditioner"

    def __init__(self, controller: SmartTemperatureController, entry: ConfigEntry) -> None:
        super().__init__(controller, entry)
        self._attr_unique_id = f"{DOMAIN}_last_mode_{entry.data['device_id']}"

    @property
    def native_value(self) -> str:
        mode_map = {"3": "cool", "4": "heat", "6": "fan", "1": "auto"}
        return mode_map.get(self._controller.last_mode, self._controller.last_mode)
