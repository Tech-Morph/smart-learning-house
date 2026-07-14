"""Config flow for Daikin Smart Temperature."""
from __future__ import annotations

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, OptionsFlow, ConfigEntry
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN, DAIKIN_DOMAIN,
    CONF_DEVICE_ID, CONF_TARGET_TEMP, CONF_TOLERANCE,
    CONF_MIN_TEMP, CONF_MAX_TEMP, CONF_POLL_INTERVAL,
    CONF_MODE_SWITCH_MIN, CONF_OVERRIDE_TIMEOUT,
    CONF_LEARNING_ENABLED,
    CONF_MORNING_OFFSET, CONF_DAY_OFFSET, CONF_EVENING_OFFSET, CONF_NIGHT_OFFSET,
    CONF_FAN_CLOSE_DELTA, CONF_FAN_MID_DELTA,
    DEFAULT_TARGET_TEMP, DEFAULT_TOLERANCE, DEFAULT_MIN_TEMP, DEFAULT_MAX_TEMP,
    DEFAULT_POLL_INTERVAL, DEFAULT_MODE_SWITCH_MIN, DEFAULT_OVERRIDE_TIMEOUT,
    DEFAULT_LEARNING_ENABLED,
    DEFAULT_MORNING_OFFSET, DEFAULT_DAY_OFFSET, DEFAULT_EVENING_OFFSET, DEFAULT_NIGHT_OFFSET,
    DEFAULT_FAN_CLOSE_DELTA, DEFAULT_FAN_MID_DELTA,
)


class DaikinSmartTempConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle the initial setup flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}

        # Collect available Daikin devices from the sister integration
        daikin_data = self.hass.data.get(DAIKIN_DOMAIN, {})
        devices: dict[str, str] = {}  # device_id -> friendly name
        for entry_id, coordinators in daikin_data.items():
            for coord in coordinators:
                devices[coord.device_id] = coord.device_name

        if not devices:
            return self.async_abort(reason="no_daikin_devices")

        if user_input is not None:
            await self.async_set_unique_id(f"{DOMAIN}_{user_input[CONF_DEVICE_ID]}")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=f"Smart Temp — {devices[user_input[CONF_DEVICE_ID]]}",
                data={CONF_DEVICE_ID: user_input[CONF_DEVICE_ID]},
            )

        schema = vol.Schema({
            vol.Required(CONF_DEVICE_ID): vol.In(devices),
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        return DaikinSmartTempOptionsFlow(config_entry)


class DaikinSmartTempOptionsFlow(OptionsFlow):
    """Options flow — all tuning params editable from the UI."""

    def __init__(self, entry: ConfigEntry) -> None:
        self._entry = entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        o = self._entry.options

        schema = vol.Schema({
            vol.Optional(CONF_TARGET_TEMP,      default=o.get(CONF_TARGET_TEMP,      DEFAULT_TARGET_TEMP)):      vol.Coerce(float),
            vol.Optional(CONF_TOLERANCE,        default=o.get(CONF_TOLERANCE,        DEFAULT_TOLERANCE)):        vol.Coerce(float),
            vol.Optional(CONF_MIN_TEMP,         default=o.get(CONF_MIN_TEMP,         DEFAULT_MIN_TEMP)):         vol.Coerce(float),
            vol.Optional(CONF_MAX_TEMP,         default=o.get(CONF_MAX_TEMP,         DEFAULT_MAX_TEMP)):         vol.Coerce(float),
            vol.Optional(CONF_LEARNING_ENABLED, default=o.get(CONF_LEARNING_ENABLED, DEFAULT_LEARNING_ENABLED)): bool,
            vol.Optional(CONF_MORNING_OFFSET,   default=o.get(CONF_MORNING_OFFSET,   DEFAULT_MORNING_OFFSET)):   vol.Coerce(float),
            vol.Optional(CONF_DAY_OFFSET,       default=o.get(CONF_DAY_OFFSET,       DEFAULT_DAY_OFFSET)):       vol.Coerce(float),
            vol.Optional(CONF_EVENING_OFFSET,   default=o.get(CONF_EVENING_OFFSET,   DEFAULT_EVENING_OFFSET)):   vol.Coerce(float),
            vol.Optional(CONF_NIGHT_OFFSET,     default=o.get(CONF_NIGHT_OFFSET,     DEFAULT_NIGHT_OFFSET)):     vol.Coerce(float),
            vol.Optional(CONF_FAN_CLOSE_DELTA,  default=o.get(CONF_FAN_CLOSE_DELTA,  DEFAULT_FAN_CLOSE_DELTA)):  vol.Coerce(float),
            vol.Optional(CONF_FAN_MID_DELTA,    default=o.get(CONF_FAN_MID_DELTA,    DEFAULT_FAN_MID_DELTA)):    vol.Coerce(float),
            vol.Optional(CONF_POLL_INTERVAL,    default=o.get(CONF_POLL_INTERVAL,    DEFAULT_POLL_INTERVAL)):    vol.All(vol.Coerce(int), vol.Range(min=30)),
            vol.Optional(CONF_MODE_SWITCH_MIN,  default=o.get(CONF_MODE_SWITCH_MIN,  DEFAULT_MODE_SWITCH_MIN)):  vol.All(vol.Coerce(int), vol.Range(min=60)),
            vol.Optional(CONF_OVERRIDE_TIMEOUT, default=o.get(CONF_OVERRIDE_TIMEOUT, DEFAULT_OVERRIDE_TIMEOUT)): vol.All(vol.Coerce(int), vol.Range(min=0)),
        })
        return self.async_show_form(step_id="init", data_schema=schema)
