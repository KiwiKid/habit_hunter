import json
import logging
import voluptuous as vol
from datetime import date, datetime, timedelta

from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.discovery import async_load_platform

REQUIREMENTS = []

_LOGGER = logging.getLogger(__name__)

CONF_ATTRIBUTION = ""
CONF_HABITS = "habits"
CONF_NAME = 'name'

DEFAULT_NAME = 'habit_tracker'
DEFAULT_ICON = 'mdi:checkbox-marked-circle-outline'

SCAN_INTERVAL = timedelta(minutes=5)
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HABITS): cv.ensure_list,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
})

async def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    name = config.get(CONF_NAME)
    habits = config.get(CONF_HABITS)

    async_add_devices(
        [HabitTrackerSensor(hass, name, habits)], update_before_add=True)

class HabitTrackerSensor(Entity):

    def __init__(self, hass, name, habits):
        """Initialize the sensor."""
        self._hass = hass
        self._name = name
        self._habits = habits
        self._state = None
        self._icon = DEFAULT_ICON
        self.update()

    @property
    def extra_state_attributes(self):
        """Return extra attributes."""
        attr = {}
        attr["habits"] = self._habits
        return attr

    def update(self):
        """Update the state."""
        # This can be any logic to determine the state of the habits.
        # For the sake of this boilerplate, it will simply count the habits.
        self._state = len(self._habits)
        return self._state

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self._icon
