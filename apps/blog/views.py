from django.shortcuts import render, get_object_or_404, redirect


from .models import Post

from django.shortcuts import render, get_object_or_404, redirect
from .models import Post


# Create your views here.
def index(request):
    
    posts = Post.objects.all()

    
    context = {
        'posts': posts,

    }
    
    return render(request, 'blog/index.html', context)

def post(request, post_id):
    # post = Post.objects.get(id=post_id)
    
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post,
    }
    return render(request, 'blog/post.html', context)
    

