from django.urls import path

from . import views

app_name = 'dogs'

urlpatterns = [
    path('cadastrar/', views.create_dog, name='create'),
]