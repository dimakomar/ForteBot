from django.apps import AppConfig
from bot import jobs

class BotConfig(AppConfig):
    name = 'bot'
    verbose_name = "Forte Bot"
    def ready(self):
        print("hello I'm ready")
        jobs.start_due()
