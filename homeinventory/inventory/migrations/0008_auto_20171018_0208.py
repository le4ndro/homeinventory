# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-18 02:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_auto_20171018_0145'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='warranty_contact_info',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='warranty_expiration',
            field=models.DateTimeField(null=True),
        ),
    ]