from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver   
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from nicky.base import Nicky

class Photos(models.Model):
    photo = ProcessedImageField(upload_to= 'feed_photos',
                                processors=[ResizeToFill(600, 800)],
                                options={'quality': 90})
class Feed(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)
    anonymous = models.BooleanField(default=False)
    author = models.ForeignKey(User, null=True, on_delete= models.CASCADE) 
    sunny_content =models.CharField(max_length=256)
    cloudy_content= models.CharField(max_length=256)
    rainy_content=models.CharField(max_length=256)
    sunny_users = models.ManyToManyField(User, blank=True, related_name='feeds_sunny', through='Sunny')
    cloudy_users = models.ManyToManyField(User, blank=True, related_name='feeds_cloudy', through='Cloudy')
    rainy_users = models.ManyToManyField(User, blank=True, related_name='feeds_rainy', through='Rainy')
    nickname=models.CharField(max_length=200, blank=True)
    feed_photos = models.ManyToManyField(Photos, related_name='feed_photo')
    hashtag_str=models.TextField(blank=True)
    result= models.CharField(default='not confirmed', max_length=200) #결과 확정. 

    def update_date(self):
        self.updated_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Notification(models.Model):
    title= models.CharField(max_length=256)
    message= models.TextField()
    viewed= models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

class Profile(models.Model):   
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    nickname = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    age = models.CharField(max_length=20, blank=True)
    lovestatus= models.CharField(max_length=20, blank=True)
    profile_photo = ProcessedImageField(upload_to= 'profile_photos',
                                        processors=[ResizeToFill(300, 400)],
                                        options={'quality': 90})               
    score= models.IntegerField(default= 0) #user 등급 위한 점수 관리

    def __str__(self):  
        return 'id=%d, user id=%d, gender=%s, nickname=%s, age=%s' % (self.id, self.user.id, self.gender, self.nickname, self.age)

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
    liked_users = models.ManyToManyField(User, blank=True, related_name='comments_liked', through='CommentLike') 
    disliked_users = models.ManyToManyField(User, blank=True, related_name='comments_disliked', through='CommentDislike')
    
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

class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE )
    comment = models.ForeignKey(FeedComment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CommentDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    comment = models.ForeignKey(FeedComment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)



