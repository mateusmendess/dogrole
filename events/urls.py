from django.urls import path

from . import views

app_name = 'events'

urlpatterns = [
    path('propor/<int:match_id>/', views.propose_event, name='propose'),
    path('responder/<int:event_id>/', views.respond_event, name='respond'),
]