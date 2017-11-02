# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-29 01:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import homeinventory.inventory.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0010_itemattachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemattachment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=models.SET(homeinventory.inventory.models.get_sentinel_user), to=settings.AUTH_USER_MODEL),
        ),
    ]