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
    return render(request, 'Vinus/about.html')

################################################################################
class DeviceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Device

    def test_func(self):
        if self.request.user == self.get_object().user:
            return True
        return False



class DeviceCreateView(LoginRequiredMixin, CreateView):
    model = Device
    fields = ['device_name', 'thinger_username', 'token', 'is_connected']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DeviceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Device
    fields = ['device_name', 'thinger_username', 'token', 'is_connected']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        Device = self.get_object()
        if self.request.user == Device.user:
            return True
        return False
################################################################################
class THINGER_APICreateView(LoginRequiredMixin, CreateView):
    model = THINGER_API
    fields = ['thinger_api_name', 'device']



################################################################################
class ResourcesCreateView(LoginRequiredMixin, CreateView):
    model = Resources
    fields = ['resources_name', 'type', 'thinger_api']
