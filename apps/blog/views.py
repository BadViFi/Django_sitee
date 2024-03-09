from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#Paginator
from django.core.paginator import Paginator





# Create your views here.
# @login_required
def index(request):
    
    posts = Post.objects.filter(is_published=True)
    create_form = PostForm()
    
    paginator = Paginator(posts, 3)
    
    context = {
        'posts': paginator.get_page(request.GET.get('page')),
        'create_form': create_form,
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
            messages.success(request, 'Пост створено')
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
            comment.author = request.user
            comment.save()
            messages.success(request, 'Коментар додано')
    return redirect('blog:post', post_id=post_id)

@login_required
def like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    post.save()
    return JsonResponse({'likes': post.likes.count()})

@login_required
def dis_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.dis_likes += 1
    post.save()
    return JsonResponse({'dis_likes': post.dis_likes})

@login_required
def like_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post__id=post_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    comment.save()
    return JsonResponse({'likes': comment.likes.count()})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.delete()
    messages.success(request, 'Пост видалено')
    return redirect('members:profile')


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пост відредаговано')
            return redirect('blog:post', post_id=post_id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})