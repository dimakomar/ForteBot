import sys
from django.apps import AppConfig


class BotConfig(AppConfig):
    name = 'bot'
    verbose_name = "Forte Bot"
    def ready(self):
        print("wsgi.started")
        # if 'bot.wsgi' in sys.argv:
        from bot import jobs
            # print("aaaa")}
        #jobs.start_due()            
        # you must import your modules here 
        # to avoid AppRegistryNotReady exception 
        
        # staxrtup code here
        
