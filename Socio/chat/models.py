from django.db import models
from django.conf import settings
from groups.models import *
User=settings.AUTH_USER_MODEL

class ChatRoom(models.Model):
    eid = models.CharField(max_length=64, unique=True)
    members = models.ManyToManyField(User)
    group = models.OneToOneField(Group, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.eid


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom,on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name="chat_sender",on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True, db_index=True)
    text = models.TextField()
    def to_data(self):
        out = {}
        out['id'] = self.id
        out['from'] = self.user
        out['date'] = self.date
        out['text'] = self.text
        return out