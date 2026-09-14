from django.urls import path

from . import views

app_name = 'matching'

urlpatterns = [
    path('', views.feed, name='feed'),
    path('matches/', views.match_list, name='match_list'),
]