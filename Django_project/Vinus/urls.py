from django.urls import path
from . import views
from .views import (
    DeviceCreateView,
    THINGER_APICreateView,
    ResourcesCreateView,
    DeviceDetailView,
    DeviceUpdateView,
)
urlpatterns = [
    path('',views.home, name='Vinus-home' ),
    path('device/<int:pk>/', DeviceDetailView.as_view(), name='device-detail'),
    path('device/new/', DeviceCreateView.as_view(), name='device-create'),
    path('device/<int:pk>/update/', DeviceUpdateView.as_view(), name='device-update'),
    path('api/new/', THINGER_APICreateView.as_view(), name='api-create'),
    path('res/new/', ResourcesCreateView.as_view(), name='api-create'),
    path('about/',views.about, name='Vinus-about' ),
]
