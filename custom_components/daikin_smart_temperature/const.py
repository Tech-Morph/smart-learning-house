"""Constants for Daikin Smart Temperature."""

DOMAIN        = "daikin_smart_temperature"
DAIKIN_DOMAIN = "daikin_comfort_control"   # Sister integration domain

# Config / options keys
CONF_DEVICE_ID           = "device_id"
CONF_TARGET_TEMP         = "target_temp"          # °F
CONF_TOLERANCE           = "tolerance"             # °F
CONF_MIN_TEMP            = "min_temp"              # °F
CONF_MAX_TEMP            = "max_temp"              # °F
CONF_POLL_INTERVAL       = "poll_interval"         # seconds
CONF_MODE_SWITCH_MIN     = "mode_switch_min"       # seconds
CONF_OVERRIDE_TIMEOUT    = "override_timeout"      # seconds (0 = disabled)
CONF_LEARNING_ENABLED    = "learning_enabled"

# Time-slot option keys
CONF_MORNING_OFFSET  = "morning_offset"
CONF_DAY_OFFSET      = "day_offset"
CONF_EVENING_OFFSET  = "evening_offset"
CONF_NIGHT_OFFSET    = "night_offset"

# Fan threshold option keys
CONF_FAN_CLOSE_DELTA = "fan_close_delta"   # within this °F of target -> low fan
CONF_FAN_MID_DELTA   = "fan_mid_delta"     # within this °F -> medium fan

# Daikin fan rate codes (from daikin_comfort_control/const.py)
FAN_RATE_AUTO   = "A"
FAN_RATE_LOW    = "2"
FAN_RATE_MEDIUM = "3"
FAN_RATE_HIGH   = "4"

# Daikin mode codes
MODE_COOL = "3"
MODE_HEAT = "4"
MODE_FAN  = "6"

# Defaults
DEFAULT_TARGET_TEMP      = 72.0
DEFAULT_TOLERANCE        = 2.0
DEFAULT_MIN_TEMP         = 65.0
DEFAULT_MAX_TEMP         = 85.0
DEFAULT_POLL_INTERVAL    = 60
DEFAULT_MODE_SWITCH_MIN  = 300
DEFAULT_OVERRIDE_TIMEOUT = 1800   # 30 min
DEFAULT_LEARNING_ENABLED = True

DEFAULT_MORNING_OFFSET  =  0.0
DEFAULT_DAY_OFFSET      =  1.0
DEFAULT_EVENING_OFFSET  =  1.0
DEFAULT_NIGHT_OFFSET    = -2.0

DEFAULT_FAN_CLOSE_DELTA =  2.0
DEFAULT_FAN_MID_DELTA   =  4.0
