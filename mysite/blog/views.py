from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail
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
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, \
                            status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.getAbsoluteUrl())
            subject = f"{cd['name']} recommends you read " \
                        f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                    f"{cd['name']}\'s comment: {cd['comments']}"
            send_mail(subject, message, 'bloghendrytest@gmail.com',
                    [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
