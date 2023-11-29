from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    def __str__(self):
        return self.username
    

class UserMessages(models.Model):
    reciever = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='reciever')
    sender = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='sender')
    time_stamp = models.DateTimeField(default=timezone.now)
    message = models.TextField()

