from django.db import models
from django.conf import settings
User=settings.AUTH_USER_MODEL
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE)
    firstName = models.CharField("First Name",max_length=20)
    lastName = models.CharField("Last Name",max_length=20)
    bio = models.CharField("Short Bio", max_length=200, blank=True, null=True)
    picture = models.ImageField('Profile picture', upload_to='static/profile_pics/%Y-%m-%d/', null=True, blank=True)
    friends = models.ManyToManyField(User,related_name="friends")

    def __str__(self):
        return str(self.user) + "'s profile"



