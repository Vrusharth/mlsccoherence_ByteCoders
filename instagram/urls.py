from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('home',views.home, name='home'),
    path('loginuser',views.loginuser, name='loginuser'),
    path('accountinsight',views.accountinsight.as_view()),
    path('accountinfo',views.accountinfo.as_view()),
    path('postinsight',views.postinsight.as_view()),
    path('addpost',views.addpost.as_view()),
    path('getcommentsonpost',views.getcommentsonpost.as_view()),
    path('postinfo',views.postinfo.as_view()),

    path('createprofile',views.createprofile.as_view()),
    path('getuser/<str:pk>/',views.getuser, name='getuser'),

    path('suggestionbot',views.suggestionbot.as_view()),
]
