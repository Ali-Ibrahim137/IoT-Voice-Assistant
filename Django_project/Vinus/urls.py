from django.urls import path
from . import views
urlpatterns = [
    path('',views.home, name='Vinus-home' ),
    path('about/',views.about, name='Vinus-about' ),
]
