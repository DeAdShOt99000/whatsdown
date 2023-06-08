from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

with open('chat/default_pic/profile_pic.png', 'rb') as profile_pic:
    global pp
    pp = profile_pic.read()

class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_pic = models.BinaryField(default=pp, editable=True)
    content_type = models.CharField(max_length=100, default='image/png', help_text='The MIMEType of the file')
    friends = models.ManyToManyField('self', blank=True)
    
class Chat(models.Model):
    text = models.TextField()
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_by_set')
    received_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_by_set')
    in_group = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)