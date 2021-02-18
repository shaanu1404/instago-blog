from django.db import models
from django.contrib.auth.models import User

from blogpost.models import BlogPost

# Create your models here.
class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    reply = models.TextField(blank=True, null=True)
    likes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "replies"

    def __str__(self):
        return f"{self.user.username} on {self.post.title} at {self.timestamp}"

    def get_profile_image_url(self):
        profile = self.user.userprofile
        return profile.get_profile_image_url()