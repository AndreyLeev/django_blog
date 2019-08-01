from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(
        max_length=20000,
        help_text="Enter your bio details here."
    )

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("blog:blogger", kwargs={"pk": self.pk})    


class Post(models.Model):

    title = models.CharField(
        max_length=200,
        help_text="Enter post title here.",
    )
    post_date = models.DateField(auto_now_add=True)
    content = models.TextField(
        max_length=20000,
        help_text="Enter your blog text here.",
    )
    likes = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-post_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post", kwargs={"pk": self.pk})
    
    
class Comment(models.Model):

    content = models.TextField(
        max_length=2000,
        help_text="Enter your comment text here.",
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    comment_date = models.DateField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['comment_date']


