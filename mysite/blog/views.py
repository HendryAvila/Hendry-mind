from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
# Create your views here.
"""
def post_list(request):
    post_lists = Post.published.all()
    paginator = Paginator(post_lists,3)
    pageNumber = request.GET.get('page', 1)
    try:
        posts = paginator.page(pageNumber)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "blog/post/list.html", {"posts": posts, "page_obj": posts})
"""

class PostListViews(ListView):
    """ alternative post list base in class with the generic class ListView provided by django"""
    queryset = Post.published.all()
    template_name = "blog/post/list.html"
    context_object_name = 'posts'
    paginate_by = 3

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                            status=Post.Status.PUBLISHED,
                            slug=post,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)
    return render(request, "blog/post/detail.html", {"post": post})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
    else:
        form = EmailPostForm()
    return render(request, "blog/post/share.html", {"form": form})
