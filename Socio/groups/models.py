from django.db import models
from django.conf import settings
User=settings.AUTH_USER_MODEL

# Create your models here.
class Group(models.Model):
    admin = models.ManyToManyField(User, related_name="group_admin")
    name = models.CharField("Name", max_length=20, unique=True)
    info = models.CharField("Short Info", max_length=200, blank=True, null=True)
    picture = models.ImageField('Group picture', upload_to='static/profile_pics/%Y-%m-%d/', null=True, blank=True)
    members = models.ManyToManyField(User, related_name="group_member")

    def __str__(self):
        return str(self.name)