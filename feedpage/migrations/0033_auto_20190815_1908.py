# Generated by Django 2.1.7 on 2019-08-15 10:08

from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('feedpage', '0032_auto_20190813_2132'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', imagekit.models.fields.ProcessedImageField(upload_to='feed_photos')),
            ],
        ),
        migrations.RemoveField(
            model_name='feed',
            name='photo',
        ),
        migrations.AddField(
            model_name='profile',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='feed',
            name='feed_photos',
            field=models.ManyToManyField(null=True, related_name='feed_photo', to='feedpage.Photos'),
        ),
    ]
