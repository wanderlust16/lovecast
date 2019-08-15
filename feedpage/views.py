from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Count
from .models import Profile, Feed, FeedComment, Sunny, Cloudy, Rainy, Notifs,CommentLike, CommentDislike
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
        title = request.POST['title']
        content = request.POST['content']
        photo =  request.FILES.get('photo', False)
        sunny_content =request.POST['sunny_content']
        cloudy_content= request.POST['cloudy_content']
        rainy_content=request.POST['rainy_content']
        anonymous=request.POST.get('anonymous') == 'on'
        hashtags=request.POST['hashtags']
        nicky=Nicky()
        nickname = nicky.get_nickname()
        Feed.objects.create(title=title,content=content,author=request.user,photo=photo, sunny_content=sunny_content, cloudy_content=cloudy_content, rainy_content=rainy_content, anonymous=anonymous, nickname=nickname, hashtag_str=hashtags)
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
        feed = Feed.objects.get(id=id)
        feed.title= title
        feed.content=content
        feed.save()
        feed.update_date()
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
        feedcomment.like_set.get(user_id = request.user.id).delete()
    else:
        CommentLike.objects.create(user_id = request.user.id, feed_id=feed.id , comment_id = feedcomment.id)
    return redirect ('/home')

def comment_dislike(request, pk, cpk):
    feed= Feed.objects.get(id = pk)
    feedcomment = FeedComment.objects.get(id = cpk)
    commentdislike_list = feedcomment.commentdislike_set.filter(user_id = request.user.id)
    if commentdislike_list.count() > 0:
        feedcomment.dislike_set.get(user_id = request.user.id).delete()
    else:
        CommentDislike.objects.create(user_id = request.user.id, feed_id=feed.id , comment_id = feedcomment.id)
    return redirect ('/home')
        
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

# def feed_confirm(request, id)
#     feed = Feed.objects.get(id=id)