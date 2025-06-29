from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentsForm, SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models  import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank
from django.contrib.postgres.search import TrigramSimilarity
import logging


logger = logging.getLogger(__name__)  # Crea un logger

#Usuario -> URL -> Vista -> Modelo -> Vista -> Template -> Usuario

# Create your views here.


# Function-based view for listing posts (commented out in the code):
import logging
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from blog.models import Post
from taggit.models import Tag

# Configurar el logger
logger = logging.getLogger(__name__)

def post_list(request, tag_slug=None):
    """
    Handles the display of a list of published posts with pagination.
    Takes the `request` object and retrieves all published posts.
    Implements pagination with 5 posts per page.
    """
    logger.info("post_list view triggered for tag: %s", tag_slug or 'None')

    post_lists = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_lists = post_lists.filter(tags__in=[tag])
        logger.debug("Filtered posts by tag: %s", tag.name)

    paginator = Paginator(post_lists, 5)
    page_number = request.GET.get('page', 1)
    
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        logger.warning("PageNotAnInteger: Page number '%s' is not an integer. Serving page 1.", page_number)
        posts = paginator.page(1)
    except EmptyPage:
        logger.warning("EmptyPage: Page number '%s' is out of range. Serving last page.", page_number)
        posts = paginator.page(paginator.num_pages)
    
    logger.info("Successfully rendered post list for page %s.", page_number)
    return render(request, "blog/post/list.html", {"posts": posts, "tag": tag})



class PostListViews(ListView):
    """
    Class-based view for listing published posts using Django's generic ListView.
    Alternative to the `post_list` function-based view.
    """
    queryset = Post.published.all()  # Retrieve all published posts
    template_name = "blog/post/list.html"  # Template to render the post list
    context_object_name = 'posts'  # Name of the context variable in the template
    paginate_by = 3  # Number of posts per page

def post_detail(request, year, month, day, post):
    """
    Handles the display of a single blog post along with its comments and comment form.

    Args:
        request: HttpRequest object.
        year (int): Year of the post's publication.
        month (int): Month of the post's publication.
        day (int): Day of the post's publication.
        post (str): Slug of the post.

    Returns:
        HttpResponse: Rendered template with the post, active comments, and comment form.
    """
    logger.info("Fetching detail for post with slug: %s published on %s-%s-%s", post, year, month, day)
    post = get_object_or_404(Post,
                            status=Post.Status.PUBLISHED,
                            slug=post,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)
    comments = post.comments.filter(active=True)  # Retrieve only active comments
    form = CommentsForm()  # Instantiate an empty comment form

    #list of similar post
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.all().filter(tags__in=post_tags_ids)\
                                        .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                    .order_by('-same_tags', '-publish')[:4]
    
    logger.debug("Found %d similar posts for '%s'", len(similar_posts), post.title)
    return render(request, "blog/post/detail.html", {'post': post,
                                                    'comments': comments,
                                                    'form': form,
                                                    'similar_posts': similar_posts})

@require_POST
def post_comment(request, post_id):
    """
    Handles the submission of a comment for a specific post.

    Args:
        request: HttpRequest object containing the POST data.
        post_id (int): ID of the post being commented on.

    Returns:
        HttpResponse: Rendered template showing the post, comment form, and the saved comment.
    """
    post = get_object_or_404(Post,
                            id=post_id,
                            status=Post.Status.PUBLISHED)
    comment = None
    form = CommentsForm(data=request.POST)  # Bind the submitted data to the form
    if form.is_valid():
        # If form data is valid, save the comment without committing to the database
        comment = form.save(commit=False)
        comment.post = post  # Link the comment to the post
        comment.save()  # Save the comment to the database
        logger.info("Successfully saved comment from '%s' on post '%s'", comment.name, post.title)
    else:
        logger.warning("Invalid comment form submission for post '%s'. Errors: %s", post.title, form.errors)

    return render(request, "blog/post/comment.html",
                {
                "post": post,
                "form": form,
                "comment": comment
                })

def post_share(request, post_id):
    """
    Handles the sharing of a post via email.

    Args:
        request: HttpRequest object containing the POST data (if form submitted).
        post_id (int): ID of the post to share.

    Returns:
        HttpResponse: Rendered template showing the sharing form and success status.
    """
    # Retrieve the post by ID
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False  # Track if the email was sent

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)  # Bind submitted data to the email form
        if form.is_valid():
            # If form data is valid, send the email
            cd = form.cleaned_data  # Get cleaned data from the form
            post_url = request.build_absolute_uri(post.get_absolute_url())  
            # Build the full URL to the post
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comment: {cd['comments']}"
            try:
                send_mail(subject, message, 'bloghendrytest@gmail.com', [cd['to']])
                sent = True  # Update the sent status
                logger.info("Post '%s' successfully shared by '%s' to '%s'", post.title, cd['name'], cd['to'])
            except Exception as e:
                logger.error("Failed to send email for post '%s'. Error: %s", post.title, e)
        else:
            logger.warning("Invalid post share form submission for post '%s'. Errors: %s", post.title, form.errors)
    else:
        # If no data was submitted, display an empty form
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})

    #Usuario → Accede a /search/ → Vista muestra formulario → Usuario escribe "django" y envía → Navegador redirige a /search/?query=django → Vista procesa la búsqueda → Template muestra resultados.
def post_search(request):
    form = SearchForm(request.GET)
    query = None
    results = []
    
    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            logger.info("Executing search for query: '%s'", query)
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query)
            ).filter(similarity__gt=0.1).order_by('-similarity')
            logger.debug("Found %d results for query: '%s'", len(results), query)
        else:
            logger.debug("Search form submitted with an empty query.")
    
    return render(request, 'blog/post/search_post.html', {
        'results': results,
        'query': query,
    })