from django.shortcuts import render, get_object_or_404, redirect


from .models import Post

from .forms import PostForm



# Create your views here.
def index(request):
    
    posts = Post.objects.all()
    
    create_form = PostForm()

    
    context = {
        'posts': posts,
        'form': create_form,

    }
    
    return render(request, 'blog/index.html', context)

def post(request, post_id):
    # post = Post.objects.get(id=post_id)
    
    
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post,
    }
    return render(request, 'blog/post.html', context)
    
    
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return redirect('blog:index')

