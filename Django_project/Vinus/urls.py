from django.urls import path
from . import views
from .views import (
    DeviceCreateView,
)
urlpatterns = [
    path('devices/', views.devices, name='Vinus-devices-list'),
    path('',views.home, name='Vinus-home' ),
    path('Device/new/', DeviceCreateView.as_view(), name='device-create'),
    path('about/',views.about, name='Vinus-about' ),
]
