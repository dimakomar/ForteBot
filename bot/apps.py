import sys
from django.apps import AppConfig


class BotConfig(AppConfig):
    name = 'bot'
    verbose_name = "Forte Bot"
    def ready(self):
        if 'bot.wsgi' in sys.argv:
            return True
        # you must import your modules here 
        # to avoid AppRegistryNotReady exception 
        from bot import jobs
        print("aaaa")
        jobs.start_due()
        # startup code here
        
