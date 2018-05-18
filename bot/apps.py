import sys
from django.apps import AppConfig


class BotConfig(AppConfig):
    name = 'bot'
    verbose_name = "Forte Bot"
    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        # you must import your modules here 
        # to avoid AppRegistryNotReady exception 
        from bot import jobs
        jobs.start_due()
        # startup code here
        
