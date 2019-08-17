from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Count
from .models import Profile, Feed, FeedComment, Sunny, Cloudy, Rainy, CommentLike, CommentDislike, Photos
from django.contrib.auth.models import User
from django.db.models import F,Sum
from nicky.base import Nicky
from django.http import HttpResponse

def index(request):
    if request.method == 'GET': 
        sort = request.GET.get('sort','')
        ranking= Feed.objects.annotate(total=Count('sunny_users')+Count('cloudy_users')+Count('rainy_users')).order_by('-total','-updated_at')
        if sort == 'forecasts':
            feeds=ranking
        else:
            feeds=Feed.objects.order_by('-created_at')
        return render(request, 'feedpage/index.html', {'feeds': feeds, 'ranking':ranking})
    elif request.method == 'POST': 
        #글 POST시 점수 +해주기
        request.user.profile.score+=10  #글 하나 씩 쓸 때마다 10점 추가 
        request.user.profile.save()

        title = request.POST['title']
        content = request.POST['content']
        sunny_content =request.POST['sunny_content']
        cloudy_content= request.POST['cloudy_content']
        rainy_content=request.POST['rainy_content']
        anonymous=request.POST.get('anonymous') == 'on'
        hashtags=request.POST['hashtags']
        nicky=Nicky()
        nickname = nicky.get_nickname()
        new=Feed.objects.create(
                title=title,
                content=content,author=request.user, 
                sunny_content=sunny_content, 
                cloudy_content=cloudy_content, 
                rainy_content=rainy_content, 
                anonymous=anonymous, 
                nickname=nickname, 
                hashtag_str=hashtags, 
                )

        #사진 안 올릴 때도 가능하게 if문 추가
        if request.FILES:
            for afile in request.FILES.getlist('photo', False):
                photos = Photos()
                photos.photo=afile
                photos.save()
                new.feed_photos.add(photos)
                new.save()
        print(request.user.profile.score)
        return redirect('/home')

def new(request):
    return render(request, 'feedpage/new.html')

def show(request, id):
    if request.method == 'GET': 
        feed = Feed.objects.get(id=id)
        return render(request, 'feedpage/show.html', {'feed': feed})
    elif request.method == 'POST': 
        title = request.POST['title']
        content = request.POST['content']
        result= request.POST['result'] #수정할 때 결과 확정 
        feed = Feed.objects.get(id=id)
        feed.title= title
        feed.content=content
        feed.result=result
        feed.save()
        feed.update_date()
        if feed.result=='Sunny':
            for a in feed.sunny_users.all():
                a.profile.score+=100
                a.profile.save()
        elif feed.result=='Cloudy':
            for a in feed.cloudy_users.all():
                a.profile.score+=100
                a.profile.save()
        elif feed.result=='Rainy':
            for a in feed.rainy_users.all():
                a.profile.score+=100
                a.profile.save()
        return redirect('/home/'+str(id))

def delete(request, id):
    feed = Feed.objects.get(id=id)
    feed.delete()
    return redirect('/home')

def edit(request, id):
    feed = Feed.objects.get(id=id)
    return render(request, 'feedpage/edit.html', {'feed':feed})

def create_comment(request, id):
    content = request.POST['content']
    FeedComment.objects.create(feed_id=id, content=content, author = request.user)
    #댓글 POST시 점수 +해주기
    request.user.profile.score+=2
    request.user.profile.save()
    print(request.user.profile.score)
    return redirect('/home')

def delete_comment(request, id, cid):
    c = FeedComment.objects.get(id=cid)
    c.delete()
    return redirect('/home')

def feed_sunny(request, pk):
    feed = Feed.objects.get(id = pk)
    sunny_list = feed.sunny_set.filter(user_id = request.user.id)
    if sunny_list.count() > 0:
        feed.sunny_set.get(user_id = request.user.id).delete()
    else:
        Sunny.objects.create(user_id = request.user.id, feed_id = feed.id)
    return redirect ('/home')

def feed_cloudy(request, pk):
    feed = Feed.objects.get(id = pk)
    cloudy_list = feed.cloudy_set.filter(user_id = request.user.id)
    if cloudy_list.count() > 0:
        feed.cloudy_set.get(user_id = request.user.id).delete()
    else:
        Cloudy.objects.create(user_id = request.user.id, feed_id = feed.id)
    return redirect ('/home')

def feed_rainy(request, pk):
    feed = Feed.objects.get(id = pk)
    rainy_list = feed.rainy_set.filter(user_id = request.user.id)
    if rainy_list.count() > 0:
        feed.rainy_set.get(user_id = request.user.id).delete()
    else:
        Rainy.objects.create(user_id = request.user.id, feed_id = feed.id)
    return redirect ('/home')

def mypage(request):
    feeds = Feed.objects.all()
    return render(request, 'feedpage/mypage.html', {'feeds':feeds})

def search(request): # 해쉬태그 검색 + 결과보여주는 함수
    feeds=Feed.objects.all()
    hashtags = request.GET.get('hashtags','')
    for f in feeds:
        keyword=f.hashtag_str.split("#")[1:]
        if hashtags in keyword:
            feeds= feeds.filter(hashtag_str__icontains=hashtags)
            return render(request, 'feedpage/search.html', {'feeds':feeds})

def comment_like(request, pk, cpk):
    feed= Feed.objects.get(id = pk)
    feedcomment = feed.feedcomment_set.get(id = cpk)
    commentlike_list = feedcomment.commentlike_set.filter(user_id = request.user.id)
    if commentlike_list.count() > 0:
        feedcomment.commentlike_set.get(user_id = request.user.id).delete()
    else:
        CommentLike.objects.create(user_id = request.user.id, feed_id=feed.id , comment_id = feedcomment.id)
    return redirect ('/home')

def comment_dislike(request, pk, cpk):
    feed= Feed.objects.get(id = pk)
    feedcomment = FeedComment.objects.get(id = cpk)
    commentdislike_list = feedcomment.commentdislike_set.filter(user_id = request.user.id)
    if commentdislike_list.count() > 0:
        feedcomment.commentdislike_set.get(user_id = request.user.id).delete()
    else:
        CommentDislike.objects.create(user_id = request.user.id, feed_id=feed.id , comment_id = feedcomment.id)
    return redirect ('/home')

'''
def notify(request):
    new = Notifs.objects.filter(user=request.user)
    if new:
        new.update(timestamp=timezone.now())
    else:
        Notifs.objects.create(user=request.user, timestamp=timezone.now())
    last_checked = Notifs.objects.values_list('timestamp', flat=True).get(user=request.user)
    forecasts= Sunny.objects.filter(feed__user = request.user, created_at__gte=last_checked).order_by('-id')
    print(forecasts)
    return render(request, 'feedpage/notify.html', {'forecasts': forecasts})
'''
