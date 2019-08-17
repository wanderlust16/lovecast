from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Count
from .models import Profile, Feed, FeedComment, Sunny, Cloudy, Rainy, CommentLike, CommentDislike, Photos, Notification
from django.contrib.auth.models import User
from django.db.models import F,Sum
from nicky.base import Nicky
from django.http import HttpResponse

def index(request):
    if request.method == 'GET': 
        notifs= Notification.objects.filter(user=request.user, viewed=False)
        sort = request.GET.get('sort','')
        ranking= Feed.objects.annotate(total=Count('sunny_users')+Count('cloudy_users')+Count('rainy_users')).order_by('-total','-updated_at')
        
        if sort == 'forecasts':
            feeds=ranking
        else:
            feeds=Feed.objects.order_by('-created_at')
        return render(request, 'feedpage/index.html', {'feeds': feeds, 'ranking':ranking, 'notifs':notifs})
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
        nickname = nicky.get_nickname()[0]
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
        
        return redirect('/home')

def new(request):
    notifs= Notification.objects.filter(user=request.user, viewed=False)
    return render(request, 'feedpage/new.html', {'notifs':notifs} )

def show(request, id):
    if request.method == 'GET': 
        feed = Feed.objects.get(id=id)
        notifs= Notification.objects.filter(user=request.user, viewed=False)
        return render(request, 'feedpage/show.html', {'feed': feed, 'notifs':notifs})
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
    notifs= Notification.objects.filter(user=request.user, viewed=False)
    feed = Feed.objects.get(id=id)
    return render(request, 'feedpage/edit.html', {'feed':feed, 'notifs': notifs})

def create_comment(request, id):
    content = request.POST['content']
    feed= Feed.objects.get(id=id)
    FeedComment.objects.create(feed_id=id, content=content, author = request.user)
    #댓글 POST시 점수 +해주기
    request.user.profile.score+=2
    request.user.profile.save()
    #게시글 주인한테 알림 띄우기
    Notification.objects.create(
        title= '',
        message= '['+feed.title +']'+ "  에 댓글이 달렸습니다",
        user= feed.author,
    )
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
    Notification.objects.create(
        title= '',
        message= '['+feed.title +']'+ '  에 예보가 달렸습니다',
        user= feed.author
    )
    return redirect ('/home')

def feed_cloudy(request, pk):
    feed = Feed.objects.get(id = pk)
    cloudy_list = feed.cloudy_set.filter(user_id = request.user.id)
    if cloudy_list.count() > 0:
        feed.cloudy_set.get(user_id = request.user.id).delete()
    else:
        Cloudy.objects.create(user_id = request.user.id, feed_id = feed.id)
    Notification.objects.create(
        title= '',
        message= '['+feed.title +']'+ '  에 예보가 달렸습니다',
        user= feed.author
    )
    return redirect ('/home')

def feed_rainy(request, pk):
    feed = Feed.objects.get(id = pk)
    rainy_list = feed.rainy_set.filter(user_id = request.user.id)
    if rainy_list.count() > 0:
        feed.rainy_set.get(user_id = request.user.id).delete()
    else:
        Rainy.objects.create(user_id = request.user.id, feed_id = feed.id)
    Notification.objects.create(
        title= '',
        message= '['+feed.title +']'+ '  에 예보가 달렸습니다',
        user= feed.author
    )
    return redirect ('/home')

def mypage(request):
    feeds = Feed.objects.all()
    notifs= Notification.objects.filter(user=request.user, viewed=False)
    return render(request, 'feedpage/mypage.html', {'feeds':feeds, 'notifs':notifs})

def search(request): # 해쉬태그 검색 + 결과보여주는 함수
    feeds=Feed.objects.all()
    notifs= Notification.objects.filter(user=request.user, viewed=False)
    hashtags = request.GET.get('hashtags','')
    for f in feeds:
        keyword=f.hashtag_str.split("#")[1:]
        if hashtags in keyword:
            feeds= feeds.filter(hashtag_str__icontains=hashtags)
            return render(request, 'feedpage/search.html', {'feeds':feeds, 'notifs':notifs})

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

def profile_edit(request):
    if request.method == 'GET': 
        return render(request, 'feedpage/profile_edit.html')
    elif request.method == 'POST': 
        nickname = request.POST['nickname']
        lovestatus = request.POST['lovestatus']
        profile_photo = request.FILES.get('profile_photo', False)
        request.user.profile.nickname=nickname
        request.user.profile.lovestatus=lovestatus
        request.user.profile.profile_photo=profile_photo
        request.user.profile.save()
        return redirect('/home/mypage')

def show_notifications(request):
    notifs= Notification.objects.filter(user=request.user, viewed=False)
    return render(request, 'base.html', {'notifs': notifs})

def delete_notifications(request, nid):
    notif= Notification.objects.get(id=nid)
    notif.delete()
    return redirect('/home')

