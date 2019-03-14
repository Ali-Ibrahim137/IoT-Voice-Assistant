from django.contrib import messages
from django.shortcuts import render
from .forms import Record
from Vinus.models import Device, THINGER_API, Resources
from Vinus.views import ConnectWithThinger
from django.contrib.auth.decorators import login_required
import requests
import json
@login_required
def record(request):
    if request.method == 'POST':
        form = Record(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            form = Record()
            if len(text) < 5 or text[0:5]!= "vinus":
                return render(request, 'record/record.html', {'form': form})
            devices = ParseText.get_device_name(text, request.user)
            user_devices = Device.objects.filter(user = request.user)
            if len(devices) == 0 and len(user_devices) !=1:
                messages.warning(request, 'No device name was recognized')
                return render(request, 'record/record.html', {'form': form})
            if len(devices) > 1 and len(user_devices) !=1:
                messages.warning(request, 'More than one device recognized')
                return render(request, 'record/record.html', {'form': form})
            if len(devices) == 1:
                device = devices.pop()
            else:
                device = Device.objects.get(user = request.user)
            is_connected =ConnectWithThinger.get_is_connected(device.thinger_username,
                                                              device.device_name,
                                                              device.token)
            if is_connected == -2:
                messages.warning(request, 'UNAUTHORIZED')
                return render(request, 'record/record.html', {'form': form})
            if is_connected == 0:
                device.is_connected = False
                device.save()
                messages.warning(request, 'Device not connected')
                return render(request, 'record/record.html', {'form': form})
            device.is_connected = True
            print (device.device_name)
            device.save()
            # Extracted the device_name and device is connected

            apis = set()
            apis = ParseText.get_thinger_api(text, device)

            Apis = THINGER_API.objects.filter(device = device)

            if len(apis) == 0 and len(Apis)!=2:
                messages.warning(request, 'No Api name was recognized')
                return render(request, 'record/record.html', {'form': form})
            if len(apis) > 1 and len(Apis)!=2:
                messages.warning(request, 'More than one Api name recognized')
                return render(request, 'record/record.html', {'form': form})
            if len(apis) == 1:
                api = apis.pop()
            else:
                for cur_api in Apis:
                    if cur_api.thinger_api_name != "api":
                        api = cur_api

            print (api.thinger_api_name)
            # Extracted the api

            # print(device)
            # url = "http://localhost/v2/users/qwerty/devices/qwerty/print"
            # x = {
            #   "R": text
            # }
            # payload = json.dumps(x)
            # headers = {
            #     'authorization': "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJWaW51cyIsInVzciI6InF3ZXJ0eSJ9.DatV-lDlNTkFQ3LZhkkz8m6VKUNQc5wb4vkoE88a7y0",
            #     'content-type': "application/json"
            # }
            # response = requests.request("POST", url, data=payload, headers=headers)
            return render(request, 'record/record.html', {'form': form})
    else:
        form = Record()
    return render(request, 'record/record.html', {'form': form})


class ParseText:
    @classmethod
    def get_device_name(cls, text, user):
        devices = Device.objects.filter(user = user)
        words = text.split(' ')
        ret = set()
        for word in words:
            for device in devices:
                if device.device_name == word:
                    ret.add(device)
        l = len(words)
        for i in range(1, l):
            word = words[i-1] + '_' +words[i]
            for device in devices:
                if device.device_name == word:
                    ret.add(device)

        return ret
    @classmethod
    def get_thinger_api(cls, text, device):
        apis = THINGER_API.objects.filter(device = device)
        words = text.split(' ')
        ret = set()
        for word in words:
            for api in apis:
                if api.thinger_api_name == word:
                    ret.add(api)
        l = len(words)
        for i in range(1, l):
            word = words[i-1] + '_' +words[i]
            for api in apis:
                if api.thinger_api_name == word:
                    ret.add(api)

        return ret
