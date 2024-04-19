from django.shortcuts import render, HttpResponse
from apps.order.models import Cart
from django.contrib.auth.models import User







def index(request):
    user_id = request.user.id
    return render(request, 'main/index.html', {'an': Cart.objects.filter(user_id=user_id).count })

def about(request):
    return render(request,'main/aboutt.html')

def home(request):
    return render(request, 'main/contact.html')

