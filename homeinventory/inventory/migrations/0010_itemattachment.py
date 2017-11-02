# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-29 00:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import homeinventory.inventory.models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_auto_20171022_1202'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.FileField(upload_to=homeinventory.inventory.models.user_directory_path)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Item')),
            ],
        ),
    ]