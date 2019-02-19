from django.contrib import admin
from django.http import HttpResponse
# Create your views here.

def home(request):
    return HttpResponse('<h1>Vinus Home Page</h1>')
def about(request):
    return HttpResponse('<h1>About Vinus</h1>')
