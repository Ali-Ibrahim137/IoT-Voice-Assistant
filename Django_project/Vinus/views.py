from django.http import HttpResponse
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
import json
import requests
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
        is_connected = ConnectWithThinger.get_is_connected(form.instance.thinger_username,
                                                           form.instance.device_name,
                                                           form.instance.token)
        if is_connected == -1:
            response = super().form_invalid(form)
            messages.warning(self.request, 'No such Device in Your Thinger.io Account!')
            return response
        if is_connected == -2:
            response = super().form_invalid(form)
            messages.warning(self.request, 'UNAUTHORIZED')
            return response

        form.instance.is_connected = is_connected
        devices = Device.objects.filter(device_name =form.instance.device_name, user=self.request.user)
        if not devices.exists():
            return super().form_valid(form)
        response = super().form_invalid(form)
        messages.warning(self.request, 'Cant have two devices with the same name')
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
        is_connected = ConnectWithThinger.get_is_connected(form.instance.thinger_username,
                                                           form.instance.device_name,
                                                           form.instance.token)
        if is_connected ==-1:
            response = super().form_invalid(form)
            messages.warning(self.request, 'No such Device in Your Thinger.io Account!')
            return response
        if is_connected == -2:
            response = super().form_invalid(form)
            messages.warning(self.request, 'UNAUTHORIZED')
            return response
        form.instance.is_connected = is_connected

        devices = Device.objects.filter(device_name = form.instance.device_name, user=self.request.user)
        if not devices.exists():
            return super().form_valid(form)
        devices = Device.objects.filter(device_name = form.instance.device_name,
                                        user = self.request.user,
                                        thinger_username = form.instance.thinger_username,
                                        token = form.instance.token
                                        )
        if not devices.exists():
            return super().form_valid(form)
        response = super().form_invalid(form)
        messages.warning(self.request, 'Cant have two devices with the same name')
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
    def form_valid(self, form):
        device = form.instance.device
        thinger_username = device.thinger_username
        device_name = device.device_name
        token = device.token
        thinger_api_name = form.instance.thinger_api_name
        exists = ConnectWithThinger.get_api_exists(thinger_username, device_name, token, thinger_api_name)
        if exists == 1:
            return super().form_valid(form)
        if exists == 0:
            response = super().form_invalid(form)
            messages.warning(self.request, 'No such API in Your Thinger.io Device!')
            return response
        response = super().form_invalid(form)
        messages.warning(self.request, 'UNAUTHORIZED')
        return response



# THINGER_APIUpdateView:
# url: api/<int:pk>/update
# template_name = 'thinger_api_form.html'
# Updates existing api
class THINGER_APIUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = THINGER_API
    fields = ['thinger_api_name', 'device']
    def form_valid(self, form):
        device = form.instance.device
        thinger_username = device.thinger_username
        device_name = device.device_name
        token = device.token
        thinger_api_name = form.instance.thinger_api_name
        exists = ConnectWithThinger.get_api_exists(thinger_username, device_name, token, thinger_api_name)
        if exists == 1:
            return super().form_valid(form)
        if exists == 0:
            response = super().form_invalid(form)
            messages.warning(self.request, 'No such API in Your Thinger.io Device!')
            return response
        response = super().form_invalid(form)
        messages.warning(self.request, 'UNAUTHORIZED')
        return response

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
# template_name = 'thinger-res-list.html'
# Lists all the Resources for some API
class ApiResListView(ListView):
    model = THINGER_API
    template_name='Vinus/thinger-res-list.html'
    def get_queryset(self):
        thinger_api=get_object_or_404(THINGER_API, thinger_api_name=self.kwargs.get('thinger_api_name'))
        return Resources.objects.filter(thinger_api = thinger_api)


######################## THINGER_API Views ends here ###########################
################################################################################
######################### Resources Views starts here ##########################

# ResourcesDetailView:
# url: /res/<int:pk>/detail
# template_name = 'resources_detail.html'
# Contain Resources info
class ResourcesDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Resources
    def test_func(self):
        Resources = self.get_object()
        if self.request.user == Resources.thinger_api.device.user:
            return True
        return False

# ResourcesCreateView:
# url: /res/new
# template_name = 'resources_form.html'
# Creates new Resource
class ResourcesCreateView(LoginRequiredMixin, CreateView):
    model = Resources
    fields = ['resources_name', 'type', 'data_type' ,'thinger_api']

    def form_valid(self, form):
        res = Resources.objects.filter(thinger_api = form.instance.thinger_api,
                                       data_type = form.instance.data_type)
        if res.exists():
            response = super().form_invalid(form)
            messages.warning(self.request, 'Cant have two Resources with the same data type!')
            return response
        return super().form_valid(form)
# ResourcesUpdateView:
# url: /res/<int:pk>/update
# template_name = 'resources_form.html'
# Updates existing Resource
class ResourcesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Resources
    fields = ['resources_name', 'type', 'data_type' ,'thinger_api']

    def form_valid(self, form):
        form.instance.user = self.request.user
        res = Resources.objects.filter(thinger_api = form.instance.thinger_api,
                                       data_type = form.instance.data_type)
        if res.exists():
            response = super().form_invalid(form)
            messages.warning(self.request, 'Cant have two Resources with the same data type!')
            return response
        return super().form_valid(form)
    def test_func(self):
        Resources = self.get_object()
        if self.request.user == Resources.thinger_api.device.user:
            return True
        return False

# ResourcesDeleteView:
# url: /res/<int:pk>/delete
# template_name = 'resources_confirm_delete.html'
# Deletes existing Resource
class ResourcesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Resources
    success_url = '/'

    def test_func(self):
        Resources = self.get_object()
        if self.request.user == Resources.thinger_api.device.user:
            return True
        return False

########################## Resources Views ends here ###########################
################################################################################
################################################################################
################################################################################
######################## ConnectWithThinger starts here ########################

def Refresh_Devices(request):
    user = request.user
    devices = Device.objects.filter(user = user)
    for device in devices:
        thinger_username = device.thinger_username
        device_name = device.device_name
        token = device.token
        is_connected = ConnectWithThinger.get_is_connected(thinger_username, device_name, token)
        if is_connected == -1:
            messages.warning(request, 'Device ' + device_name + ' not in your Thinger Account any more, it was deleted!')
            device.delete()
        if is_connected == -2:
            messages.warning(request, 'UNAUTHORIZED for device ' + device_name)
        if is_connected==0 or is_connected ==1:
            device.is_connected = is_connected
            device.save()
    return HttpResponse()
class ConnectWithThinger:
    @classmethod
    def get_is_connected(cls, thinger_username, device_name, token):
        try:
            url = "http://localhost/v1/users/" + thinger_username + "/devices"
            payload = ""
            headers = {'authorization': 'Bearer '+ token}
            response = requests.request("GET", url, data=payload, headers=headers)
            response = response.text
            res = json.loads(response)
            for device in res:
                if device["device"] == device_name:
                    return device["connection"]["active"]
            return -1
        except Exception as e:
            return -2
    @classmethod
    def get_api_exists(cls, thinger_username, device_name, token, thinger_api_name):
        try:
            url = 'http://localhost/v2/users/'+thinger_username + '/devices/'+device_name + '/api'
            payload = ""
            headers = {'authorization': 'Bearer '+ token}
            response = requests.request("GET", url, data=payload, headers=headers)
            response = response.text
            res = json.loads(response)
            for api in res:
                if api == thinger_api_name:
                    return True
            return False
        except Exception as e:
            return -1
