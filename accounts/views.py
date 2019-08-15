from django.shortcuts import render
from django.contrib.auth.models import User
from feedpage.models import Profile
from django.contrib import auth
from django.shortcuts import redirect

def signup(request):
    if request.method  == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                username=request.POST['username'], 
                password=request.POST['password1'])
            nickname= request.POST['nickname']
            gender= request.POST['gender']
            age= request.POST['age']
            lovestatus= request.POST['lovestatus']
            profile_photo = request.FILES.get('profile_photo', False)
            for user in User.objects.all():
                if hasattr(user,'Profile') and not user.Profile:
                    profile= Profile(user=user)
                    profile.save()
            user.profile.nickname=nickname
            user.profile.age=age
            user.profile.gender=gender
            user.profile.lovestatus=lovestatus
            user.profile.profile_photo=profile_photo
            auth.login(request, user)
            return redirect('/home')
    return render(request, 'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('/home')
        else:
            return render(request, 'accounts/login.html', {'error' : 'email or password is incorrect'})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    return render(request, 'accounts/login.html')