from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from blog.models import Post, Comment, Category, Feedback
from blog.forms import PostForm, CommentForm
from datetime import datetime
from django.db.models import Avg

def post_list(request):
    posts = Post.objects.all().filter(published_1=True)
    category = Category.objects.all()
    counter = posts.count()
    context = {'items': posts, 'category': category, 'counter':counter}
    return render(request, 'blog/post_list.html', context)

def categories(request, category_pk):
    posts = Post.objects.filter(category=category_pk)
    category = Category.objects.all()
    return render(request, 'blog/post_list.html', {'items': posts, 'category': category})

def post_draft(request):
    posts = Post.objects.all().filter(published_1=False)
    category = Category.objects.all()
    counter = posts.count()
    return render(request, 'blog/post_list.html', {'items': posts, 'counter': counter})

def post_publish(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post.published_1 = 'True'
    post.save()
    return redirect('post_list')


def rating(post_pk):
    fback = Feedback.objects.filter(post=post_pk)
    count = sum([i.rating for i in fback]) / fback.count()
    return round(count, 1)


def post_detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    comment = Comment.objects.all().filter(post=post_pk)
    counter = comment.count()
    a_rate = rating(post_pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.publish_date = datetime.now()
            comment.save()
            return redirect('post_detail', post_pk=post.pk)
    else:
        comment_form = CommentForm()
    context = {'post': post,
               'comment': comment,
               'counter': counter,
               'comment_form': comment_form,
               'rating': a_rate}
    return render(request, 'blog/post_detail.html', context)

def post_new(request):
    if request.method == "GET":
        form = PostForm
        return render(request, 'blog/post_new.html', {"form": form})
    else:
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.create_date = datetime.now()
            post.publish_date = datetime.now()
            post.save()
            return redirect('post_detail', post_pk=post.pk)

def post_edit(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == "GET":
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {"form": form})
    else:
        form = PostForm(request.POST, instance=post) #instance=post чтоб изменялся старый а не создавался новый
        if form.is_valid():
            post = form.save(commit=False)
            post.create_date = datetime.now()
            post.publish_date = datetime.now()
            post.save()
            return redirect('post_detail', post_pk=post.pk)

def post_delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk).delete()
    return redirect('post_list')

def comment_delete(request, post_pk, comment_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = Comment.objects.all().filter(pk=post_pk)
    comment = Comment.objects.get(pk=comment_pk).delete()
    return redirect('post_detail', post_pk=post.pk)

def feedback(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    fback = Feedback.objects.filter(post=post_pk)
    return render(request, 'blog/feedback.html', {
        'fback': fback, 'post': post})

#отображать посты с самым высоким рейтенгом
def recommends(request):
    posts = Post.objects.values('title', 'pk').annotate(Avg('feedbacks__rating')).order_by('-feedbacks__rating__avg')[0:5]
    return render(request, 'blog/post_list.html', {'items': posts})

def myposts(request):
    post = Post.objects.filter(author=request.user)
    return render(request, 'blog/post_myposts.html', {'items': post})