from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

from .models import Post,Comment

from .forms import PostForm,CommentForm
from django.contrib.auth.decorators import login_required



# Create your views here.
def index(request):
    
    posts = Post.objects.all()
    
    create_form = PostForm()
    
    counter = Post.objects.count()



    
    context = {
        'posts': posts,
        'form': create_form,
        'post_count' : counter

    }
    
    return render(request, 'blog/index.html', context)


@login_required
def post(request, post_id):
    # post = Post.objects.get(id=post_id)
    
    form_comment = CommentForm()
    post = get_object_or_404(Post, id=post_id)
    post.views += 1
    post.save()
    context = {
        'post': post,
        "comment_form" : form_comment,
    }
    return render(request, 'blog/post.html', context)
    
@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
    return redirect('blog:index')

@login_required
def comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            print(comment)
            comment.post = post
            comment.save()
    return redirect('blog:post', post_id=post_id)

@login_required
def like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.likes += 1
    post.save()
    return JsonResponse({'likes': post.likes})

@login_required
def dis_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.dis_likes += 1
    post.save()
    return JsonResponse({'dis_likes': post.dis_likes})





def like_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.likes += 1
    comment.save()
    return JsonResponse({'likes': comment.likes})