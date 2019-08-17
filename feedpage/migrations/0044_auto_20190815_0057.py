# Generated by Django 2.2.3 on 2019-08-14 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedpage', '0043_auto_20190815_0034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feed',
            name='photo',
        ),
        migrations.AddField(
            model_name='feed',
            name='feed_photos',
            field=models.ManyToManyField(blank=True, related_name='feed_photo', to='feedpage.Photos'),
        ),
    ]