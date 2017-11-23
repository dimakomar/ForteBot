from django.db import models


class User(object):
    model.
    user_id = models.CharField(max_length=100)
    dm_channel = models.CharField(max_length=100)

    def __init__(self, user_id, dm_channel):
        self.user_id = user_id
        self.dm_channel = dm_channel
