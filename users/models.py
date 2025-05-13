from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count, Q
class User(AbstractUser):
    # extend later if needed
    pass

class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    bio         = models.TextField(blank=True)
    skills      = models.ManyToManyField('skills.Skill', blank=True, related_name='holders')

    def __str__(self):
        return self.user.username

    @property
    def reputation_score(self):
        agg = self.votes.aggregate(
            up=Count('id', filter=Q(upvote=True)),
            down=Count('id', filter=Q(upvote=False)),
        )
        return (agg['up'] or 0) - (agg['down'] or 0)
