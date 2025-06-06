from django.db import models
from django.conf import settings

class Notification(models.Model):
    user    = models.ForeignKey(
                  settings.AUTH_USER_MODEL,
                  on_delete=models.CASCADE,
                  related_name='notifications'
              )
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notify {self.user.username}: {self.message[:20]}"
