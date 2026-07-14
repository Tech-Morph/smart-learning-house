# 🏠 Daikin Comfort Control Smart Temperature

A Home Assistant custom integration (HACS-compatible) that adds autonomous,
learning-based temperature management on top of
[Daikin Comfort Control](https://github.com/Tech-Morph/daikin_comfort_control).

It reads `htemp` (indoor temp) directly from the existing
`daikin_comfort_control` coordinator — **no second cloud connection, no
extra sensors, no MQTT**. When the temperature drifts outside your comfort
band, it issues mode + fan + setpoint commands back through the same API.

## Features

- 🧠 Time-of-day learning slots with per-slot temperature offsets
- 🌡️ Automatic mode selection (cool / heat / fan-only)
- 💨 Dynamic fan speed based on how far you are from target
- ⏱️ Compressor short-cycle protection (configurable minimum switch interval)
- 🔕 Manual override detection — pauses automation if you touch the Daikin app/remote
- 📊 Switch entity to enable/disable automation from Lovelace
- 🔧 All settings configurable via HA Options flow (no YAML required)
- ✅ Zero extra hardware, zero extra API accounts

## Requirements

- [Daikin Comfort Control](https://github.com/Tech-Morph/daikin_comfort_control)
  custom integration already installed and configured
- Home Assistant 2024.1+

## Installation (HACS)

1. In HACS → Integrations → ⋮ → Custom Repositories
2. Add `https://github.com/Tech-Morph/smart-learning-house`, category: Integration
3. Install **Daikin Comfort Control Smart Temperature**
4. Restart Home Assistant
5. Settings → Devices & Services → Add Integration → search **Daikin Smart Temperature**
6. Select your Daikin device (auto-discovered from `daikin_comfort_control`)

## Entities Created

| Entity | Type | Description |
|---|---|---|
| `switch.daikin_smart_temp_<id>` | Switch | Enable / disable automation |
| `sensor.daikin_smart_temp_target_<id>` | Sensor | Current effective target temp |
| `sensor.daikin_smart_temp_mode_<id>` | Sensor | Last commanded mode |

## Options (via UI)

- Target temperature, tolerance, min/max bounds
- Time-slot offsets (morning / day / evening / night)
- Fan speed thresholds
- Poll interval, mode-switch minimum interval, override timeout

## License

MIT
