from django.db import models
from django.conf import settings
from groups.models import *
from message import sha1
User=settings.AUTH_USER_MODEL

# Create your models here.
class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name="post_owner")
    group = models.ForeignKey(Group,on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='static/posts', null=True, blank=True)
    file = models.FileField(upload_to='posts/uploads/',null=True,blank=True)
    sha1 = models.CharField(max_length=20,null=True)
    likes = models.ManyToManyField(User,related_name="post_likes")
    date = models.DateTimeField(auto_now=True, db_index=True)

    def filepath(self):
        f = str(self.file)
        return f[14:]

    def getSha1(self):
        if self.file:
            data = open(str(self.file), 'rb')
            sha = sha1.sha1(data)
            return sha
        else:
            return None

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE, related_name="comment_post")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_owner")
    text = models.CharField(max_length=100)


