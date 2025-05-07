from django.db import models
from users.models import Profile

class Vote(models.Model):
    voter     = models.ForeignKey(Profile, on_delete=models.CASCADE)
    profile   = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='votes')
    upvote    = models.BooleanField(default=True)  # up/down
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter','profile')
