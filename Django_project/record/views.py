from django.http import JsonResponse
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

Output_API = 1
Integer_Data = 1
Input_API  = 2
Double_Data  = 2
Input_Outpur_API = 3
Bool_Data  = 3
No_Parameters_API = 4
Other_Data = 4
other = 5
Global_thinger_username = ""
Global_device_name = ""
Global_thinger_api_name = ""
Global_resources_name = ""
Global_token = ""

@login_required
def record(request):
    type = request.GET.get('type', None)
    text = request.GET.get('message', None)
    text = str(text)
    text = text.lower()
    tokenize = nltk.word_tokenize(text)
    if (len(tokenize) !=0 and tokenize[0]!='none') or type=="speak":
        form = Record()
        return ParseText.Handle(tokenize, text, form, type, request)
    if request.method == 'POST':
        form = Record(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            form = Record()
            text = text.lower()
            tokenize = nltk.word_tokenize(text)
            return ParseText.Handle(tokenize, text, form, "text",request)
    else:
        form = Record()
    return render(request, 'record/record.html', {'form': form})


def speak(text, type = 0):
    data = {
        'text': text,
        'type': type
    }
    return JsonResponse(data)

def editDistDP(str1, str2, m, n):
    dp = [[0 for x in range(n+1)] for x in range(m+1)]
    for i in range(m+1):
        for j in range(n+1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i][j-1],        # Insert
                                   dp[i-1][j],        # Remove
                                   dp[i-1][j-1])      # Replace
    return dp[m][n]



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


    @classmethod
    def get_data(cls, data, data_type, request, form):
        if data_type == Integer_Data:
            nums = re.findall(r'(?<!\S)[+-]?\d+(?!\S)', data)
            if len(nums)==1:
                num = nums[0]
                return num
            return "INVALID"
        if data_type == Double_Data:
            nums = re.findall(r"[+-]?\d+(?:\.\d+)?",data)
            if len(nums)==1:
                num = nums[0]
                return num
            return "INVALID"
        if data_type == Bool_Data:
            turn_on  = 0
            turn_off = 0
            tokenize = nltk.word_tokenize(data)
            l = len(tokenize)
            for i in range (1,l):
                if tokenize[i-1] + ' ' + tokenize [i] == "turn on":
                    turn_on = 1
                if tokenize[i-1] + ' ' + tokenize [i] == "turn off":
                    turn_off = 1
            if turn_on == turn_off:
                return "INVALID"
            if turn_on == 1:
                return 1
            if turn_off == 1:
                return 0
        # data_type = other     will be handled later
        if data_type == Other_Data:
            return "*"

    @classmethod
    def Handle(cls, tokenize, text , form, type ,request):
        global other, Global_thinger_username, Global_device_name, Global_thinger_api_name, Global_resources_name, Global_token
        f = 0;
        for i in tokenize:
            i = i.lower()
            if editDistDP(i, 'vinus', len(i), 5) <= 3:
                f = 1
            if editDistDP(i, 'okay', len(i), 4) <= 2:
                f = 1

        if f == 0:
            if type =='speak':
                return speak("*")
            return render(request, 'record/record.html', {'form': form})

        devices = ParseText.get_device_name(tokenize, request.user)
        user_devices = Device.objects.filter(user = request.user)
        if len(devices) == 0 and other == 1:
            other = 0
            # this is the other data
            value = tokenize[1]
            l = len(tokenize)
            for i in range(2,l):
                value+= (' ' + tokenize[i])
            ConnectWithThinger.send_to_thinger(Global_thinger_username, Global_device_name,
                                               Global_thinger_api_name, Global_resources_name,
                                               value, Global_token, Other_Data)
            Global_thinger_username = ""
            Global_device_name = ""
            Global_thinger_api_name = ""
            Global_resources_name = ""
            Global_token = ""
            if type =='speak':
                return speak("the command has been executed")
            messages.warning(request, 'Other data was sent !')
            return render(request, 'record/record.html', {'form': form})

        other = 0
        if len(devices) == 0 and len(user_devices) !=1:
            if type =='speak':
                return speak("incomplete command")
            messages.warning(request, 'No device name was recognized')
            return render(request, 'record/record.html', {'form': form})

        if len(devices) > 1 and len(user_devices) !=1:
            if type =='speak':
                return speak("incomplete command")
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
            if type =='speak':
                return speak("unauthorized")
            messages.warning(request, 'UNAUTHORIZED')
            return render(request, 'record/record.html', {'form': form})
        if is_connected == 0:
            device.is_connected = False
            device.save()
            if type =='speak':
                return speak("device not connected")
            messages.warning(request, 'Device not connected')
            return render(request, 'record/record.html', {'form': form})
        device.is_connected = True
        device.save()
        # Extracted the device_name and device is connected
        apis = set()
        apis = ParseText.get_thinger_api(tokenize, device)
        Apis = THINGER_API.objects.filter(device = device)
        if len(apis) == 0 and len(Apis)!=2:
            if type =='speak':
                return speak("incomplete command")
            messages.warning(request, 'No Api name was recognized')
            return render(request, 'record/record.html', {'form': form})
        if len(apis) > 1 and len(Apis)!=2:
            if type =='speak':
                return speak("incomplete command")
            return render(request, 'record/record.html', {'form': form})
            messages.warning(request, 'More than one Api name recognized')
        if len(apis) == 1:
            api = apis.pop()
        else:
            for cur_api in Apis:
                if cur_api.thinger_api_name != "api":
                    api = cur_api
        # Extracted the api
        # iterate through all the Resources for this api
        # for every data_type check if there is some value in the text
        # ask a question for the other value
        resources = Resources.objects.filter(thinger_api = api)
        thinger_username = device.thinger_username
        device_name = device.device_name
        thinger_api_name = api.thinger_api_name
        token = device.token

        if api.type == Input_API:
            # input api
            # extract the value, and send the value to thinger.io
            res = Resources.objects.get(thinger_api = api)
            data = ParseText.get_data(text, res.data_type, request, form)
            if data=="*":
                other = 1
                Global_thinger_username = thinger_username
                Global_device_name = device_name
                Global_thinger_api_name = thinger_api_name
                Global_resources_name = res.resources_name
                Global_token = token
                if type =='speak':
                    return speak("What is the " + res.resources_name, 1)
                messages.warning(request, 'More than one Api name recognized')
                return render(request, 'record/record.html', {'form': form})
            if data == "INVALID":
                if type =='speak':
                    return speak("incomplete command")
                messages.warning(request, 'No data was extracted!')
                return render(request, 'record/record.html', {'form': form})

            resources_name = res.resources_name
            value = data
            ConnectWithThinger.send_to_thinger(thinger_username, device_name, thinger_api_name,
                                               resources_name, value, token, res.data_type)
            if type =='speak':
                return speak("the command has been executed")

            return render(request, 'record/record.html', {'form': form})
        if api.type == Output_API:
            # output api
            # Get data from the thinger.io
            res = Resources.objects.get(thinger_api = api)
            resources_name = res.resources_name
            value = ConnectWithThinger.get_from_thinger(thinger_username, device_name,
                                                        thinger_api_name, resources_name ,token)
            if type =='speak':
                return speak("the value of " + thinger_api_name + " is " + str(value))
            messages.success(request, 'The value of ' + thinger_api_name + ' is ' + str(value))
            return render(request, 'record/record.html', {'form': form})
        if api.type == No_Parameters_API:
            # no parameters api
            # Send a request to thinger to execute this api
            ConnectWithThinger.execute_no_par(thinger_username, device_name, thinger_api_name, token)
            if type =='speak':
                return speak("the command has been executed")
            return render(request, 'record/record.html', {'form': form})
        if api.type == Input_Outpur_API:
            # input output API
            # first send the input value to thinger.io
            # then  read the output value from thinger.io
            in_res = Resources.objects.get(thinger_api = api, type = 2)     # 2 is input res
            data = ParseText.get_data(text, in_res.data_type, request, form)
            if data == "INVALID":
                if type =='speak':
                    return speak("incomplete command")
                messages.warning(request, 'No data was extracted!')
                return render(request, 'record/record.html', {'form': form})
            value = data
            out_res = Resources.objects.get(thinger_api = api, type = 1)     # 1 is output res
            value = ConnectWithThinger.send_get(thinger_username, device_name, in_res, data, out_res, thinger_api_name, token, in_res.data_type)
            messages.success(request, 'The value of ' + out_res.resources_name + ' is ' + str(value))
            if type =='speak':
                return speak("the value of " + out_res.resources_name + " is " + str(value))
            return render(request, 'record/record.html', {'form': form})







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
