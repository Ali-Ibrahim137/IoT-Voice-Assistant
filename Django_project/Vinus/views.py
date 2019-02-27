from django.contrib import messages
from django.shortcuts import render, get_object_or_404,  redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Device, THINGER_API, Resources
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
################################################################################
# home page, contains devices for logged In user
def home(request):
    if not request.user.is_authenticated:
        return render(request, 'Vinus/home.html')
    context = {
        'object_list': Device.objects.filter(user = request.user)
    }
    return render(request, 'Vinus/home.html', context)

# about page
def about(request):
    return render(request, 'Vinus/about.html')

################################################################################
########################### Devices Views start here ###########################

# DeviceDetailView:
# url: /device/<int:pk>/detail
# template_name = 'device_detail.html'
# Contain device info, without the apis
class DeviceDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Device
    def test_func(self):
        if self.request.user == self.get_object().user:
            return True
        return False

# DeviceCreateView:
# url: /device/new
# template_name = 'device_form.html'
# Creates new device
class DeviceCreateView(LoginRequiredMixin, CreateView):
    model = Device
    fields = ['device_name', 'thinger_username', 'token']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.is_connected = False      # TODO: get this vlue from the Thinger.io server
        devices = Device.objects.filter(device_name =form.instance.device_name, user=self.request.user)
        if not devices.exists():
            return super().form_valid(form)
        response = super().form_invalid(form)
        messages.warning(self.request, 'cant have two devices with the same name')
        return response

# DeviceUpdateView:
# url: /device/<int:pk>/update
# template_name = 'device_form.html'
# Updates existing device
class DeviceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Device
    fields = ['device_name', 'thinger_username', 'token']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.is_connected = False      # TODO: get this vlue from the Thinger.io server
        devices = Device.objects.filter(device_name =form.instance.device_name, user=self.request.user)
        cnt = 0
        for device in devices:
            cnt = cnt+1
            if cnt==2:
                break
        if(cnt <= 1):
            return super().form_valid(form)
        response = super().form_invalid(form)
        messages.warning(self.request, 'cant have two devices with the same name')
        return response

    def test_func(self):
        Device = self.get_object()
        if self.request.user == Device.user:
            return True
        return False

# DeviceDeletView:
# url: /device/<int:pk>/delete
# template_name = 'device_confirm_delete.html'
# Deletes existing device
class DeviceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Device
    success_url = '/'

    def test_func(self):
        Device = self.get_object()
        if self.request.user == Device.user:
            return True
        return False

# DeviceApiListView:
# url: /device/<str:device_name>
# template_name = 'device-api-list.html.html'
# Lists all the APIs for some device
class DeviceApiListView(ListView):
    model = Device
    template_name='Vinus/device-api-list.html'
    def get_queryset(self):
        device=get_object_or_404(Device, device_name=self.kwargs.get('device_name'))
        return THINGER_API.objects.filter(device=device)


########################### Devices Views ends here ############################
################################################################################
######################## THINGER_API Views starts here #########################

# THINGER_APIDetailView:
# url: /api/<int:pk>/detail
# template_name = 'thinger_api_detail.html'
# Contain API info, without the resources
class THINGER_APIDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = THINGER_API
    def test_func(self):
        THINGER_API = self.get_object()
        if self.request.user == THINGER_API.device.user:
            return True
        return False


# THINGER_APICreateView:
# url: /device/new
# template_name = 'thinger_api__form.html'
# Creates new API
class THINGER_APICreateView(LoginRequiredMixin, CreateView):
    model = THINGER_API
    fields = ['thinger_api_name', 'device']

# THINGER_APIUpdateView:
# url: api/<int:pk>/update
# template_name = 'thinger_api_form.html'
# Updates existing api
class THINGER_APIUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = THINGER_API
    fields = ['thinger_api_name', 'device']

    def test_func(self):
        THINGER_API = self.get_object()
        if self.request.user == THINGER_API.device.user:
            return True
        return False

# THINGER_APIDeleteView:
# url: /api/<int:pk>/delete
# template_name = 'thinger_api_confirm_delete.html'
# Deletes existing api
class THINGER_APIDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = THINGER_API
    success_url = '/'

    def test_func(self):
        THINGER_API = self.get_object()
        if self.request.user == THINGER_API.device.user:
            return True
        return False

# ApiResListView:
# url: /api/<str:thinger_api_name>
# template_name = 'api-res-list.html.html'
# Lists all the Resources for some API
class ApiResListView(ListView):
    model = THINGER_API
    template_name='Vinus/api-res-list.html'
    def get_queryset(self):
        thinger_api=get_object_or_404(THINGER_API, thinger_api_name=self.kwargs.get('thinger_api_name'))
        return Resources.objects.filter(thinger_api = thinger_api)

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
#//////////////////////////
