"""
Daikin Comfort Control Smart Temperature

HA custom integration that wraps daikin_comfort_control's coordinator to
provide autonomous, learning-based climate control.

Dependency: daikin_comfort_control must be set up first.
"""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, DAIKIN_DOMAIN
from .smart_controller import SmartTemperatureController

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SWITCH, Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry."""
    daikin_data = hass.data.get(DAIKIN_DOMAIN, {})
    if not daikin_data:
        raise ConfigEntryNotReady(
            "daikin_comfort_control is not loaded. Install and configure it first."
        )

    device_id = entry.data["device_id"]
    coordinator = None
    for entry_id, coordinators in daikin_data.items():
        for coord in coordinators:
            if coord.device_id == device_id:
                coordinator = coord
                break

    if coordinator is None:
        raise ConfigEntryNotReady(
            f"Daikin device '{device_id}' not found in daikin_comfort_control. "
            "Ensure the base integration is set up."
        )

    # Pass entry_id, NOT the entry object itself — controller always resolves
    # the live entry from hass.config_entries so options changes are seen
    # immediately without a restart.
    controller = SmartTemperatureController(hass, entry.entry_id, coordinator)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = controller

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    controller.start()

    # Re-notify entities when options are saved so Lovelace updates instantly
    entry.async_on_unload(
        entry.add_update_listener(_async_options_updated)
    )

    return True


async def _async_options_updated(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Called by HA when the user saves new options. Refreshes entity states."""
    _LOGGER.debug("Options updated for %s — notifying entities", entry.entry_id)
    controller: SmartTemperatureController = hass.data[DOMAIN].get(entry.entry_id)
    if controller:
        controller.options_updated()


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        controller: SmartTemperatureController = hass.data[DOMAIN].pop(entry.entry_id)
        controller.stop()
    return unload_ok
