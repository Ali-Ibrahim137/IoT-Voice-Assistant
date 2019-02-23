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
    if not request.user.is_authenticated:
        return render(request, 'Vinus/home.html')
    context = {
        'object_list': Device.objects.filter(user = request.user)
    }
    return render(request, 'Vinus/home.html', context)

def about(request):
    return render(request, 'Vinus/about.html', {'title':'about'})
