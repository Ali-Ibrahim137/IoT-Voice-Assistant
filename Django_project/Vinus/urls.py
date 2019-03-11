from django.urls import path
from . import views
from .views import (
    DeviceCreateView,
    DeviceDetailView,
    DeviceUpdateView,
    DeviceDeleteView,
    DeviceApiListView,

    THINGER_APICreateView,
    THINGER_APIDetailView,
    THINGER_APIUpdateView,
    THINGER_APIDeleteView,
    ApiResListView,

    ResourcesCreateView,
    ResourcesDetailView,
    ResourcesUpdateView,
    ResourcesDeleteView,
)
urlpatterns = [
    path('',views.home, name='Vinus-home' ),
    path('about/',views.about, name='Vinus-about' ),
    path('Refresh_Devices/', views.Refresh_Devices, name='refresh-devices'),
    path('device/new/', DeviceCreateView.as_view(), name='device-create'),
    path('device/<int:pk>/detail/', DeviceDetailView.as_view(), name='device-detail'),
    path('device/<int:pk>/update/', DeviceUpdateView.as_view(), name='device-update'),
    path('device/<int:pk>/delete/', DeviceDeleteView.as_view(), name='device-delete'),
    path('device/<str:device_name>/', DeviceApiListView.as_view(), name='device-api-list'),

    path('api/new/', THINGER_APICreateView.as_view(), name='api-create'),
    path('api/<int:pk>/detail/', THINGER_APIDetailView.as_view(), name='api-detail'),
    path('api/<int:pk>/update/', THINGER_APIUpdateView.as_view(), name='api-update'),
    path('api/<int:pk>/delete/', THINGER_APIDeleteView.as_view(), name='api-delete'),
    path('api/<str:thinger_api_name>/', ApiResListView.as_view(), name='api-res-list'),

    path('res/new/', ResourcesCreateView.as_view(), name='res-create'),
    path('res/<int:pk>/detail/', ResourcesDetailView.as_view(), name='res-detail'),
    path('res/<int:pk>/update/', ResourcesUpdateView.as_view(), name='res-update'),
    path('res/<int:pk>/delete/', ResourcesDeleteView.as_view(), name='res-delete'),
]
