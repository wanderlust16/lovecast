# Generated by Django 2.2.3 on 2019-08-09 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedpage', '0011_auto_20190808_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='age',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
