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
    WARRANTY_CHOICES = (
        ('001', 'original manufacturer warranty'),
        ('002', 'insurance warranty underwritten and regulated as insurance'),
        ('003', 'lifetime warranty'),
        ('004', 'satisfaction guarantee'),
        ('005', 'implied warranty'),
        ('006', 'other'),
    )
    #name = models.CharField(max_length=100)
    make = models.CharField(max_length=255, null=True)
    model = models.CharField(max_length=255)
    id_number = models.CharField(max_length=255, null=True)
    purchased_from = models.CharField(max_length=255, null=True)
    purchased_date = models.DateTimeField(null=True)
    quantity = models.IntegerField(null=True)
    value = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    estimated_current_value = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    description = models.CharField(max_length=500)
    attributes = models.CharField(max_length=500, null=True)
    notes = models.CharField(max_length=500, null=True)
    year = models.IntegerField(null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    warranty = models.BooleanField(default=False)
    warranty_type = models.CharField(max_length=3, choices=WARRANTY_CHOICES, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        null=True
    )

    def __str__(self):
        return self.model
