from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # extend later if needed
    pass

class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    bio         = models.TextField(blank=True)
    skills      = models.ManyToManyField('skills.Skill', blank=True, related_name='holders')

    def __str__(self):
        return self.user.username
