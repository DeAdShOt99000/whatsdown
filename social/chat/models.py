from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Chat(models.Model):
    message = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_set')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_set')
    date_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.sender.username} -> {self.receiver.username}'