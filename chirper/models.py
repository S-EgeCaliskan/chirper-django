from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    text = models.TextField(max_length=300)
    date_added = models.DateTimeField(auto_now_add=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text
    
class Reply(models.Model):
    text = models.TextField(max_length=300)
    date_added = models.DateTimeField(auto_now_add=True)
    replier = models.ForeignKey(User, on_delete=models.CASCADE)
    post_to_reply = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "replies"
    
    def __str__(self):
        return self.text

