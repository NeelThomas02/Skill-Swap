from django.db import models
from users.models import Profile

class Message(models.Model):
    sender    = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='msgs_sent')
    receiver  = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='msgs_received')
    text      = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
