from django.urls import path
from . import views
urlpatterns = [
    path('devices/', views.devices, name='Vinus-devices-list'),
    path('',views.home, name='Vinus-home' ),
    path('about/',views.about, name='Vinus-about' ),
]
