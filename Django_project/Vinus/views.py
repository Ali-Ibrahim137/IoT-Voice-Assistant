from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Device, THINGER_API, Resources

def home(request):
    return render(request, 'Vinus/home.html')

def about(request):
    return render(request, 'Vinus/about.html', {'title':'about'})

def devices(request):
    context = {
        'object_list': Device.objects.filter(userr = request.user)
    }
    return render (request, 'Vinus/device_list.html', context)
