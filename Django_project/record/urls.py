from django.urls import path
from . import views

urlpatterns = [
    path('record/', views.record, name = 'record'),
]
