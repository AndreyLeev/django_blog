from django.urls import path
from .views import *

app_name = 'blog'
urlpatterns = [
    path("", index, name="index"),
    path("blog/", index, name="index"),
    path("blog/post-create/", post_create, name="post_create"),
    path("blog/account", user_sign_up, name="account"),
    path("blogs/", PostsListView.as_view(), name="posts"),
    path("bloggers/", AuthorsListView.as_view(), name="bloggers"),
    path("bloggers/<int:pk>/", BlogerView.as_view(), name="blogger"),
    path("blogs/<int:pk>/", PostView.as_view(), name="post"),
    path("blogs/<int:pk>/comment/", comment_create, name="comment_create"),
    path("blogs/<int:pk>/comments-list/", CommentsListView.as_view(), name="comments"),
]
