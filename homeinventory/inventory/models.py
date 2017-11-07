import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from homeinventory.core.models import TimeStampedModel


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


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

    make = models.CharField(max_length=255, null=True, blank=True)
    model = models.CharField(max_length=255)
    id_number = models.CharField(max_length=255, null=True, blank=True)
    purchased_from = models.CharField(max_length=255, null=True, blank=True)
    purchased_date = models.DateTimeField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    value = models.DecimalField(max_digits=9, decimal_places=2, null=True,
                                blank=True)
    estimated_current_value = models.DecimalField(max_digits=9,
                                                  decimal_places=2,
                                                  null=True,
                                                  blank=True)
    description = models.CharField(max_length=500)
    attributes = models.CharField(max_length=500,
                                  null=True, blank=True)
    notes = models.CharField(max_length=500, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)
    warranty = models.BooleanField(default=False, blank=True)
    warranty_type = models.CharField(max_length=3, choices=WARRANTY_CHOICES,
                                     null=True, blank=True)
    warranty_expiration = models.DateTimeField(null=True, blank=True)
    warranty_contact_info = models.CharField(max_length=1000, null=True,
                                             blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        null=True
    )

    def __str__(self):
        return self.model

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'pk': self.pk})


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/uploads/user_<id>/<filename>
    return 'uploads/user_{0}/{1}'.format(instance.user.id, filename)


class ItemAttachment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    upload = models.FileField(upload_to=user_directory_path)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        null=True
    )

    @property
    def filename(self):
        return os.path.basename(self.upload.name)


class ItemPhoto(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    upload = models.ImageField(upload_to=user_directory_path)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        null=True
    )

    @property
    def filename(self):
        return os.path.basename(self.upload.name)
