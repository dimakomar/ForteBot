from django.db import models

# Create your models here.
class Message(models.Model):
    # id = models.AutoField()
    text = models.TextField(null=False, db_index=True)
    number = models.IntegerField()

    def __str__(self):
        return self.text