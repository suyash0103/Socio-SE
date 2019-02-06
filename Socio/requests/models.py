from django.db import models
from django.conf import settings
User=settings.AUTH_USER_MODEL
# Create your models here.

class Request(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name="request_sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,related_name="request_receiver")
    date = models.DateTimeField(auto_now=True, db_index=True)
