import sys
from django.apps import AppConfig


class BotConfig(AppConfig):
    some = 1
    name = 'bot'
    verbose_name = "Forte Bot"
    def ready(self):
        pass
        print("wsgi.started")
        # if 'bot.wsgi' in sys.argv:
        from bot import jobs
            # print("aaaa")}
        jobs.start_due()            
        # you must import your modules here 
        # to avoid AppRegistryNotReady exception 
        
        # staxrtup code here
        
