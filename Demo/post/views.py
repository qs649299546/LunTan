from math import ceil

from django.core.cache import cache
from django.shortcuts import render, redirect

from post.models import Post, Comment, Tag, PostTags
from post.helper import page_cache
from post.helper import rds
from post.helper import get_top_n
from user.helper import check_perm


def post_list(request):
    total = Post.objects.count()  # 文章总数
    pages = ceil(total / 5)       # 总页数

    page = int(request.GET.get('page', 1))
    start = (page - 1) * 5
    end = start + 5
    posts = Post.objects.all()[start:end]  # 按索引取出当前页的文章

    return render(request, 'post_list.html',
                  {'posts': posts, 'pages': range(1, pages + 1)})


@check_perm('user')
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        uid = request.session['uid']
        post = Post.objects.create(uid=uid, title=title, content=content)
        return redirect('/post/read/?post_id=%s' % post.id)

    return render(request, 'create_post.html', {})


@check_perm('user')
def edit_post(request):
    if request.method == 'POST':
        post_id = int(request.POST.get('post_id'))
        post = Post.objects.get(id=post_id)
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()

        tags = request.POST.get('tags', '')
        tag_list = [tag.strip().title() for tag in tags.split(',')]
        PostTags.update_post_tags(post.id, tag_list)

        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        post_id = int(request.GET.get('post_id'))
        post = Post.objects.get(id=post_id)
        tags = ', '.join(t.name for t in post.tags())
        return render(request, 'edit_post.html', {'post': post, 'tags': tags})


@page_cache(1)
def read_post(request):
    post_id = int(request.GET.get('post_id'))
    post = Post.objects.get(id=post_id)
    rds.zincrby('ReadRank', post_id)

    return render(request, 'read_post.html',
                  {'post': post, 'comments': post.comments(), 'tags': post.tags()})


@check_perm('admin')
def delete_post(request):
    post_id = int(request.GET.get('post_id'))
    Post.objects.get(id=post_id).delete()
    return redirect('/')


def top10_post(request):
    rand_data = get_top_n(10)
    return render(request, 'top10.html', {'rand_data': rand_data})


def comment(request):
    if request.method == "POST":
        post_id = int(request.POST.get('post_id'))
        name = request.POST.get('name')
        content = request.POST.get('content')
        Comment.objects.create(pid=post_id, name=name, content=content)
    return redirect('/post/read/?post_id=%s' % post_id)


def tag_filter(request):
    tag_id = int(request.GET.get('tag_id', 0))
    tag = Tag.objects.get(id=tag_id)
    return render(request, 'post_list.html', {'posts': tag.posts()})
