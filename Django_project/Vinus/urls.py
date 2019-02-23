from django.urls import path
from . import views
from .views import (
    DeviceCreateView,
    THINGER_APICreateView,
)
urlpatterns = [
    path('',views.home, name='Vinus-home' ),
    path('Device/new/', DeviceCreateView.as_view(), name='device-create'),
    path('Api/new/', THINGER_APICreateView.as_view(), name='api-create'),
    path('about/',views.about, name='Vinus-about' ),
]
