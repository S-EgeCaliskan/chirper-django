from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Post
from .forms import PostForm, ReplyForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.

def index(request):
    # display the most recent posts first
    posts = Post.objects.order_by("-date_added")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"posts": posts, 'page_obj': page_obj}
    return render(request, 'chirper/index.html',  context)

@login_required
def new_post(request):
    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(data=request.POST)
        if form.is_valid:
            new_post = form.save(commit=False)
            new_post.poster = request.user
            form.save()
            return redirect('chirper:index')
    
    context = {'form': form}
    return render(request, 'chirper/new_post.html', context)

@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.poster != request.user:
        raise Http404
    else:
        if request.method != 'POST':
            form = PostForm(instance=post)
        else:
            form = PostForm(instance=post, data=request.POST)
            if form.is_valid:
                form.save()
                return redirect('chirper:index')
    context = {'post': post, 'form':form}
    return render(request, 'chirper/edit_post.html', context)


@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {'post' : post}
    if post.poster == request.user:
        if request.method != 'POST':
            return render(request, 'chirper/edit_post.html', context)
        else: 
            post.delete()   
            return redirect('chirper:index')
    else:
        raise Http404
    

@login_required
def reply(request, post_id):
    post = Post.objects.get(id=post_id)
    replies = post.reply_set.all()
    
    if request.method != 'POST':
        form = ReplyForm()
    else:
        form = ReplyForm(data=request.POST)
        if form.is_valid:
            new_reply = form.save(commit=False)
            new_reply.post_to_reply = Post.objects.get(id=post_id)
            new_reply.replier = request.user
            form.save()
            return redirect('chirper:index')
    context = {'post' : post, 'form' : form, 'replies': replies}
    return render(request, 'chirper/reply.html', context)
    
    
    
    
    
    
    
def profile(request, poster):
    posts = Post.objects.filter(poster__username=poster).order_by('-date_added')
    context = {'posts': posts, 'poster': poster }
    return render(request, 'chirper/profile.html', context)