from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    """
    Custom manager class that overrides the default queryset to filter
    only posts with a status of 'PUBLISHED'.
    """
    def get_queryset(self):
        """
        Override the default queryset to return only published posts.
        Takes the queryset from the base `models.Manager` and applies a
        filter for `status=Post.Status.PUBLISHED`.
        Returns:
            QuerySet: Filtered queryset with only published posts.
        """
        return super().get_queryset()\
                    .filter(status=Post.Status.PUBLISHED)

class Post(models.Model):
    """ 
    A model representing a blog post. 
    Takes `models.Model` to create the attributes of the class, which correspond
    to the columns of the database table.
    """
    class Status(models.TextChoices):
        """
        An inner class to define the choices for the status field.
        Provides human-readable names for the two possible post statuses:
        - 'DF' (Draft): Represents a draft post.
        - 'PB' (Published): Represents a published post.
        """
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"
    
    # Fields for the Post model
    title = models.CharField(max_length=250) 
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now, unique_for_date="publish")  
    # Date when the post was published, defaults to the current time
    created = models.DateTimeField(auto_now_add=True)  
    # Date when the post was created (automatically set on creation)
    updated = models.DateTimeField(auto_now=True)  
    # Date when the post was last updated (automatically updated)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)  
    # Status of the post (draft or published)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")  
    # Author of the post, linked to the User model, cascades on delete

    # Managers
    objects = models.Manager()  # Default manager
    published = PublishedManager()  # Custom manager to retrieve published posts only

    tags = TaggableManager()

    class Meta:
        """
        Meta class to define additional settings for the model.
        - Orders posts by publish date in descending order.
        - Adds a database index for the publish field for optimized queries.
        """
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def __str__(self):
        """
        Returns the string representation of the Post object.
        Returns:
            str: The title of the post.
        """
        return self.title
    
    def get_absolute_url(self):
        """
        Generates the absolute URL for a specific post.
        Returns:
            str: The URL string for the post detail view.
        """
        return reverse("blog:post_detail", args=[self.publish.year,
                                                self.publish.month,
                                                self.publish.day,
                                                self.slug])

class Comment(models.Model):
    """
    A model representing a comment on a blog post.
    Takes `models.Model` to define fields that map to the database table.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  
    # The post to which the comment belongs, cascades on post deletion
    name = models.CharField(max_length=80)  # Name of the comment author
    email = models.EmailField()  # Email of the comment author
    body = models.TextField()  # Content of the comment
    created = models.DateTimeField(auto_now_add=True)  
    # Date when the comment was created (set automatically on creation)
    updated = models.DateTimeField(auto_now=True)  
    # Date when the comment was last updated (updated automatically)
    active = models.BooleanField(default=True)  
    # Boolean to indicate if the comment is active

    class Meta:
        """
        Meta class to define additional settings for the Comment model.
        - Orders comments by creation date in ascending order.
        - Adds a database index for the created field for optimized queries.
        """
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]

    def __str__(self):
        """
        Returns the string representation of the Comment object.
        Returns:
            str: A formatted string showing the comment author and post title.
        """
        return f"Comment by {self.name} on {self.post}"
