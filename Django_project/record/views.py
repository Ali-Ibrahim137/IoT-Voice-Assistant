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
            devices = ParseText.get_device_name(text, request.user)
            if len(devices) == 0:
                messages.warning(request, 'No device name was recognized')
                return render(request, 'record/record.html', {'form': form})
            if len(devices) > 1:
                messages.warning(request, 'More than one device recognized')
                return render(request, 'record/record.html', {'form': form})
            device = devices.pop()
            print (device.device_name)
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
            device.is_connected = False
            device.save()
            print ('Done, device name is  ', device.device_name)
            # Extracted the device_name and device is connected

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
        if len(ret) == 1:
            return ret
        l = len(words)
        for i in range(1, l):
            word = words[i-1] + '_' +words[i]
            for device in devices:
                if device.device_name == word:
                    ret.add(device)

        return ret
