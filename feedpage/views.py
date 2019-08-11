from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Count
from .models import Profile, Feed, FeedComment, Sunny, Cloudy, Rainy
from django.contrib.auth.models import User
from django.db.models import F,Sum

def index(request):
    if request.method == 'GET': 
        feeds = Feed.objects.all()
        ranking= Feed.objects.annotate(total=Count('sunny_users')+Count('cloudy_users')+Count('rainy_users')).order_by('-total')
        return render(request, 'feedpage/index.html', {'feeds': feeds, 'ranking':ranking})
    elif request.method == 'POST': 
        title = request.POST['title']
        content = request.POST['content']
        photo =  request.FILES.get('photo', False)
        sunny_content =request.POST['sunny_content']
        cloudy_content= request.POST['cloudy_content']
        rainy_content=request.POST['rainy_content']
        anonymous=request.POST.get('anonymous') == 'on'
        Feed.objects.create(title=title,content=content,author=request.user,photo=photo, sunny_content=sunny_content, cloudy_content=cloudy_content, rainy_content=rainy_content, anonymous=anonymous)
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

def userinfo(request):
    c_user= request.user
    c_profile=Profile.objects.get(user=c_user)
    feeds = Feed.objects.all()
    return render(request, 'feedpage/mypage.html', {'feeds':feeds})


    
    