from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("self", related_name="user_following", symmetrical=False)
    following = models.ManyToManyField("self", related_name="user_followers", symmetrical=False)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)

    def __str__(self):
        return f"Post by {self.user} on {self.timestamp}"