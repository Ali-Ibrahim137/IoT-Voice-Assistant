from django.urls import path
from . import views
from .views import (
    DeviceCreateView,
    THINGER_APICreateView,
    ResourcesCreateView,
    DeviceDetailView,
)
urlpatterns = [
    path('',views.home, name='Vinus-home' ),
    path('device/<int:pk>/', DeviceDetailView.as_view(), name='device-detail'),
    path('Device/new/', DeviceCreateView.as_view(), name='device-create'),
    path('Api/new/', THINGER_APICreateView.as_view(), name='api-create'),
    path('Res/new/', ResourcesCreateView.as_view(), name='api-create'),
    path('about/',views.about, name='Vinus-about' ),
]
