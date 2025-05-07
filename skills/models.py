from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Match(models.Model):
    seeker   = models.ForeignKey('users.Profile', on_delete=models.CASCADE, related_name='matches_sent')
    helper   = models.ForeignKey('users.Profile', on_delete=models.CASCADE, related_name='matches_received')
    skill    = models.ForeignKey(Skill, on_delete=models.CASCADE)
    created  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('seeker','helper','skill')
