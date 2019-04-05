from django.db import models
from django.conf import settings
from . import sha1
import os
User=settings.AUTH_USER_MODEL


# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name="message_sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,related_name="message_receiver")
    message = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now=True, db_index=True)

class SOSMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name="sos_sender")
    date = models.DateTimeField(auto_now=True, db_index=True)


class File(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name="file_sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,related_name="file_receiver")
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to='message/uploads/')
    sha1 = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now=True, db_index=True)

    def filepath(self):
        f=str(self.file)
        return f[16:]

    def getSha1(self):
        data = open(str(self.file), 'rb')
        sha = sha1.sha1(data)
        return sha
