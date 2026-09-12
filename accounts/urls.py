from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('cadastro/', views.signup, name='signup'),
    path('inicio/', views.home, name='home'),
]