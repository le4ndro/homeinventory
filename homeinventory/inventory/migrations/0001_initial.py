# Generated by Django 3.2.5 on 2021-07-11 16:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import homeinventory.inventory.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('user', models.ForeignKey(null=True, on_delete=models.SET(homeinventory.inventory.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('make', models.CharField(blank=True, max_length=255, null=True)),
                ('model', models.CharField(max_length=255)),
                ('id_number', models.CharField(blank=True, max_length=255, null=True)),
                ('purchased_from', models.CharField(blank=True, max_length=255, null=True)),
                ('purchased_date', models.DateTimeField(blank=True, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('estimated_current_value', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('description', models.CharField(max_length=500)),
                ('attributes', models.CharField(blank=True, max_length=500, null=True)),
                ('notes', models.CharField(blank=True, max_length=500, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('warranty', models.BooleanField(blank=True, default=False)),
                ('warranty_type', models.CharField(blank=True, choices=[('001', 'original manufacturer warranty'), ('002', 'insurance warranty underwritten and regulated as insurance'), ('003', 'lifetime warranty'), ('004', 'satisfaction guarantee'), ('005', 'implied warranty'), ('006', 'other')], max_length=3, null=True)),
                ('warranty_expiration', models.DateTimeField(blank=True, null=True)),
                ('warranty_contact_info', models.CharField(blank=True, max_length=1000, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.category')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('user', models.ForeignKey(null=True, on_delete=models.SET(homeinventory.inventory.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ItemPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.ImageField(upload_to=homeinventory.inventory.models.user_directory_path)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.item')),
                ('user', models.ForeignKey(null=True, on_delete=models.SET(homeinventory.inventory.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ItemLoan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('who', models.CharField(max_length=255)),
                ('when', models.DateTimeField()),
                ('why', models.CharField(blank=True, max_length=500, null=True)),
                ('expected_return_date', models.DateField(blank=True, null=True)),
                ('returned', models.BooleanField(default=False)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.item')),
            ],
            options={
                'get_latest_by': 'id',
            },
        ),
        migrations.CreateModel(
            name='ItemAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.FileField(upload_to=homeinventory.inventory.models.user_directory_path)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.item')),
                ('user', models.ForeignKey(null=True, on_delete=models.SET(homeinventory.inventory.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.location'),
        ),
        migrations.AddField(
            model_name='item',
            name='user',
            field=models.ForeignKey(null=True, on_delete=models.SET(homeinventory.inventory.models.get_sentinel_user), to=settings.AUTH_USER_MODEL),
        ),
    ]
