from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver   
from taggit.managers import TaggableManager
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import re


class Feed(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(User, null=True, on_delete= models.CASCADE) 
    sunny_content =models.CharField(max_length=256)
    cloudy_content= models.CharField(max_length=256)
    rainy_content=models.CharField(max_length=256)
    sunny_users = models.ManyToManyField(User, blank=True, related_name='feeds_sunny', through='Sunny')
    cloudy_users = models.ManyToManyField(User, blank=True, related_name='feeds_cloudy', through='Cloudy')
    rainy_users = models.ManyToManyField(User, blank=True, related_name='feeds_rainy', through='Rainy')
    photo = ProcessedImageField(upload_to= 'feed_photos',
                                processors=[ResizeToFill(600, 800)],
                                options={'quality': 90})
    def update_date(self):
        self.updated_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Profile(models.Model):   
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(User,max_length=20, blank=True)
    age = models.CharField(User,max_length=20, blank=True)
    status= models.CharField(User,max_length=20, blank=True)
    def __str__(self):  
        return self.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):  
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):  
    instance.profile.save()

class FeedComment(models.Model):
    content = models.TextField()
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, null=True, on_delete= models.CASCADE) 
    def __str__(self):
        return str(self.id)

class Sunny(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Cloudy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Rainy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

