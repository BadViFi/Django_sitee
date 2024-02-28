from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth.decorators import login_required



from .forms import UserCreateForm
# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('members:profile')
    else:
        form = AuthenticationForm()
    return render(request, 'members/login.html', {'form': form})



@login_required
def logout_view(request):
    logout(request)
    return redirect('members:login')





def signup_view(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            login(request, user)
            return redirect('members:profile')
    else:
        form = UserCreateForm()
    return render(request, 'members/signup.html', {'form': form})


def profile_view(request):
    return render(request, 'members/profile.html')


