# Generated by Django 2.2.3 on 2019-08-11 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedpage', '0017_auto_20190811_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='anonymous',
            field=models.BooleanField(null=True),
        ),
    ]
