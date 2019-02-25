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

class DeviceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Device
    success_url = '/'

    def test_func(self):
        Device = self.get_object()
        if self.request.user == Device.user:
            return True
        return False
#///////////////////// end of device
class THINGER_APIDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = THINGER_API
    def test_func(self):
        THINGER_API = self.get_object()
        if self.request.user == THINGER_API.device.user:
            return True
        return False

class THINGER_APICreateView(LoginRequiredMixin, CreateView):
    model = THINGER_API
    fields = ['thinger_api_name', 'device']

class THINGER_APIUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = THINGER_API
    fields = ['thinger_api_name', 'device']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        THINGER_API = self.get_object()
        if self.request.user == THINGER_API.device.user:
            return True
        return False

class THINGER_APIDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = THINGER_API
    success_url = '/'

    def test_func(self):
        THINGER_API = self.get_object()
        if self.request.user == THINGER_API.device.user:
            return True
        return False
#/////////////////////// end of Api
################################################################################
class ResourcesDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Resources
    def test_func(self):
        Resources = self.get_object()
        if self.request.user == Resources.thinger_api.device.user:
            return True
        return False

class ResourcesCreateView(LoginRequiredMixin, CreateView):
    model = Resources
    fields = ['resources_name', 'type', 'thinger_api']

class ResourcesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Resources
    fields = ['resources_name', 'type', 'thinger_api']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    def test_func(self):
        Resources = self.get_object()
        if self.request.user == Resources.thinger_api.device.user:
            return True
        return False

class ResourcesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Resources
    success_url = '/'

    def test_func(self):
        Resources = self.get_object()
        if self.request.user == Resources.thinger_api.device.user:
            return True
        return False
