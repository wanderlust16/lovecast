# Generated by Django 2.2.3 on 2019-08-12 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedpage', '0015_auto_20190812_0012'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedcomment',
            old_name='comment_disliked_users',
            new_name='disliked_users',
        ),
        migrations.RenameField(
            model_name='feedcomment',
            old_name='comment_liked_users',
            new_name='liked_users',
        ),
    ]