"""Adds config flow for Habit Hunter."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv

from .api import HabitHunterApiClient
from .const import CONF_PASSWORD
from .const import CONF_USERNAME
from .const import DOMAIN

PLATFORM_SCHEMA = cv.empty_config_schema


class HabitHunterFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for habit_hunter."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        # Uncomment the next 2 lines if only a single instance of the integration is allowed:
        # if self._async_current_entries():
        #     return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            valid = await self._test_credentials(
                user_input[CONF_USERNAME], user_input[CONF_PASSWORD]
            )
            if valid:
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME], data=user_input
                )
            else:
                self._errors["base"] = "auth"

            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return HabitHunterOptionsFlowHandler(config_entry)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_USERNAME): str
                , vol.Required(CONF_PASSWORD): str
            }
            ),
            errors=self._errors,
        )

    async def _test_credentials(self, username, password):
        """Return true if credentials is valid."""
        try:
            session = async_create_clientsession(self.hass)
            client = HabitHunterApiClient(username, password, session)
            await client.async_get_data()
            return True
        except Exception:  # pylint: disable=broad-except
            pass
        return False


class HabitHunterOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler for habit_hunter."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)
        self.habits = dict(config_entry.habits)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                **{
                    vol.Required(x, default=self.habits.get(x, True)): bool
                    for x in self.habits
                },
                vol.Required('name'): str,
                vol.Required('reset_value'): int,
                vol.Required('reset_unit'): vol.In(['days', 'months', 'years'])
            }),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_USERNAME), data=self.options
        )
