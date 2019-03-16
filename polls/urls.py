from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns =[
	path('', views.VoteView.as_view(), name='vote'),
	path('signup/', views.signup, name='signup'),
	path('accounts/', include('django.contrib.auth.urls'), name='accounts'),
	path('logout/', views.logoutin, name='logoutin'),
	path('activate/<uidb64>/<token>/',
        views.activate, name='activate'),
]