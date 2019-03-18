from django.contrib import messages
from django.shortcuts import render
from .forms import Record
from Vinus.models import Device, THINGER_API, Resources
from Vinus.views import ConnectWithThinger
from django.contrib.auth.decorators import login_required
import requests
import json
import re
import nltk
@login_required
def record(request):
    if request.method == 'POST':
        form = Record(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            tokenize = nltk.word_tokenize(text)
            form = Record()
            if tokenize[0]!="vinus":
                return render(request, 'record/record.html', {'form': form})

            devices = ParseText.get_device_name(tokenize, request.user)
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
            # print (device.device_name)
            device.save()
            # Extracted the device_name and device is connected

            apis = set()
            apis = ParseText.get_thinger_api(tokenize, device)

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

            # print (api.thinger_api_name)
            # Extracted the api

            # iterate through all the Resources for this api
            # for every data_type check if there is some value in the text
            # ask a question for the other value
            Output_Res = 1
            Integer_Data = 1
            Input_Res  = 2
            Double_Data  = 2
            Input_Outpur_Res = 3
            Bool_Data  = 3
            No_Parameters_Res = 4
            Other_Data = 4
            resources = Resources.objects.filter(thinger_api = api)
            if tokenize[1] == "get":
                # read a value from the device
                # we should find an output resource
                for res in resources:
                    if res.type == Output_Res:
                        print (res.resources_name)
                        value = ConnectWithThinger.send_get_reauest(device.thinger_username,
                                                                       device.device_name,
                                                                       res.resources_name,
                                                                       device.token)
                        # got the HTTP response value
                        messages.success(request, 'The value of ' + res.resources_name + ' is ' + str(value))
                        return render(request, 'record/record.html', {'form': form})
                # nothing to get
                messages.warrning(request, 'Nothing to get')
                return render(request, 'record/record.html', {'form': form})

            orders = []
            for res in resources:
                if res.data_type == Integer_Data or res.data_type==Double:
                    nums = re.findall('\d+', text)
                    if len(nums)==1:
                        num = nums[0]
                        orders.append([res.resources_name, res.type, num])
                    continue
                if res.data_type == Other:
                    if res.type == No_Parameters_Res:
                        orders.append([res.resources_name, res.type, 0])
                        continue
                    # this will be handled later
                    continue
                if res.data_type == Bool_Data:
                    turn_on  = 0
                    turn_off = 0
                    l = len(tokenize) - 1
                    for i in range (1,l):
                        if tokenize[i-1] + tokenize [i] == "turn on":
                            turn_on = 1
                        if tokenize[i-1] + tokenize [i] == "turn off":
                            turn_off = 1
                    if turn_on == turn_off:
                        continue
                    if turn_on == 1:
                        orders.append([res.resources_name, res.type, 1])
                    if turn_off == 1:
                        orders.append([res.resources_name, res.type, 0])
                    continue


            # 1 Output Resources                    Integer
            # 2 Input Resources                     Double
            # 3 Input/Output Resources              Bool
            # 4 Resources without parameters        Other
            return render(request, 'record/record.html', {'form': form})
    else:
        form = Record()
    return render(request, 'record/record.html', {'form': form})

class ParseText:
    @classmethod
    def get_device_name(cls, text, user):
        devices = Device.objects.filter(user = user)
        ret = set()
        for word in text:
            for device in devices:
                if device.device_name == word:
                    ret.add(device)
        l = len(text)
        for i in range(1, l):
            word = text[i-1] + '_' + text[i]
            for device in devices:
                if device.device_name == word:
                    ret.add(device)

        return ret
    @classmethod
    def get_thinger_api(cls, text, device):
        apis = THINGER_API.objects.filter(device = device)
        ret = set()
        for word in text:
            for api in apis:
                if api.thinger_api_name == word:
                    ret.add(api)
        l = len(text)
        for i in range(1, l):
            word = text[i-1] + '_' + text[i]
            for api in apis:
                if api.thinger_api_name == word:
                    ret.add(api)
        return ret






class WordsToNumbers():
    __ones__ = { 'zero': 0,
                 'one':   1, 'eleven':     11,
                 'two':   2, 'twelve':     12,
                 'three': 3, 'thirteen':   13,
                 'four':  4, 'fourteen':   14,
                 'five':  5, 'fifteen':    15,
                 'six':   6, 'sixteen':    16,
                 'seven': 7, 'seventeen':  17,
                 'eight': 8, 'eighteen':   18,
                 'nine':  9, 'nineteen':   19 }

    __tens__ = { 'ten':     10,
                 'twenty':  20,
                 'thirty':  30,
                 'forty':   40,
                 'fifty':   50,
                 'sixty':   60,
                 'seventy': 70,
                 'eighty':  80,
                 'ninety':  90 }

    __groups__ = { 'thousand':  1000,
                   'million':   1000000,
                   'billion':   1000000000,
                   'trillion':  1000000000000 }

    __groups_re__ = re.compile(
        r'\s?([\w\s]+?)(?:\s((?:%s))|$)' %
        ('|'.join(__groups__))
        )

    __hundreds_re__ = re.compile(r'([\w\s]+)\shundred(?:\s(.*)|$)')
    __tens_and_ones_re__ =  re.compile(
        r'((?:%s))(?:\s(.*)|$)' %
        ('|'.join(__tens__.keys()))
        )

    def parse(self, words):
        words = words.lower()
        groups = {}
        num = 0
        for group in WordsToNumbers.__groups_re__.findall(words):
            group_multiplier = 1
            if group[1] in WordsToNumbers.__groups__:
                group_multiplier = WordsToNumbers.__groups__[group[1]]
            group_num = 0
            hundreds_match = WordsToNumbers.__hundreds_re__.match(group[0])
            tens_and_ones = None
            if hundreds_match is not None and hundreds_match.group(1) is not None:
                group_num = group_num + \
                            (WordsToNumbers.__ones__[hundreds_match.group(1)] * 100)
                tens_and_ones = hundreds_match.group(2)
            else:
                tens_and_ones = group[0]
            if tens_and_ones is None:
                num = num + (group_num * group_multiplier)
                continue
            tn1_match = WordsToNumbers.__tens_and_ones_re__.match(tens_and_ones)
            if tn1_match is not None:
                group_num = group_num + WordsToNumbers.__tens__[tn1_match.group(1)]
                if tn1_match.group(2) is not None:
                    group_num = group_num + WordsToNumbers.__ones__[tn1_match.group(2)]
            else:
                group_num = group_num + WordsToNumbers.__ones__[tens_and_ones]
            num = num + (group_num * group_multiplier)
        return num
