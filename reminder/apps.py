from django.apps import AppConfig


class ReminderConfig(AppConfig):
    name = 'reminder'

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
