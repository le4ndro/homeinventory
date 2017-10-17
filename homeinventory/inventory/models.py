from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    created and modified fields.
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        null=True
    )

    def __str__(self):
        return self.name


class Location(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        null=True
    )

    def __str__(self):
        return self.name

class Item(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    attributes = models.CharField(max_length=500)
    notes = models.CharField(max_length=500)
    year = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        null=True
    )

    def __str__(self):
        return self.name
