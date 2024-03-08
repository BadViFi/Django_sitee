from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.blog.models import Post


from .forms import UserCreateForm
from apps.blog.forms import PostForm
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
                messages.success(request, f'Ви увійшли як {username}')
                return redirect('members:profile')
    else:
        form = AuthenticationForm()
    return render(request, 'members/login.html', {'form': form})



@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Ви вийшли з системи')
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
            messages.success(request, f'Ви успішно зареєструвалися як {user.username}')
            return redirect('members:profile')
    else:
        form = UserCreateForm()
    return render(request, 'members/signup.html', {'form': form})


@login_required
def profile_view(request):
    form_create_post = PostForm()
    user = request.user
    post_count = Post.objects.filter(author=user, is_published=True).count()
    context = {
        'form_create_post': form_create_post,
        'counter': post_count
    }
    return render(request, 'members/profile.html', context)


