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
class DeviceCreateView(LoginRequiredMixin, CreateView):
    model = Device
    fields = ['device_name', 'thinger_username', 'token', 'is_connected']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
