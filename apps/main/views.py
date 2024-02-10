from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request,'main/aboutt.html')

def home(request):
    return HttpResponse("lol, privet")