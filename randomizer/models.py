from django.db import models
from django.conf import settings
from django.db.models import Count
from random import randint


class ProfileManager(models.Manager):
    def random(self):
        count = self.aggregate(ids=Count('id'))['ids']
        random_index = randint(0, count - 1)
        return self.all()[random_index]

    def random_naive(self):
        return self.all().order_by('?')[0]

class Profile(models.Model):
    name = models.CharField(unique=True, max_length=100, db_index=True)
    objects = ProfileManager()

    def __str__(self):
        return 'Profile: {}'.format(self.name)
