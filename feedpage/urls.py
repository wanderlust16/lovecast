from django.urls import path
from feedpage import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('mypage/', views.userinfo, name='mypage'), #mypage 추가
    path('<int:id>/', views.show, name='show'),
    path('<int:id>/delete/', views.delete, name='delete'),
    path('<int:id>/edit/', views.edit, name='edit'),
    path('<int:id>/comments/', views.create_comment, name='create_comment'),
    path('<int:id>/comments/<int:cid>/', views.delete_comment, name='delete_comment'),
    path('<int:pk>/sunny/', views.feed_sunny, name='sunny'),
    path('<int:pk>/cloudy/', views.feed_cloudy, name='cloudy'),
    path('<int:pk>/rainy/', views.feed_rainy, name='rainy'),
    path('<int:pk>/comments/<int:cpk>/like/', views.comment_like, name='comment_like'),
    path('<int:pk>/comments/<int:cpk>/dislike/', views.comment_dislike, name='comment_dislike'),
    
]