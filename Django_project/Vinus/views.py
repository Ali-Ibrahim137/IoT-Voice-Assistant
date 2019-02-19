from django.shortcuts import render
# Create your views here.

def home(request):
    return render(request, 'Vinus/home.html')

def about(request):
    return render(request, 'Vinus/about.html', {'title':'about'})
