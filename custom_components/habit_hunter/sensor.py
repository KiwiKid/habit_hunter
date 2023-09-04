from homeassistant.helpers.entity import Entity

class TaskSensor(Entity):
    def __init__(self, task):
        self._task = task

    @property
    def name(self):
        return self._task.name

    @property
    def state(self):
        return "completed" if self._task.last_changed else "pending"

    @property
    def device_state_attributes(self):
        return {
            "frequency": self._task.frequency,
            "priority": self._task.priority,
            "last_changed": self._task.last_changed
        }

    def complete_task(self):
        self._task.complete()
        self.schedule_update_ha_state(True)
