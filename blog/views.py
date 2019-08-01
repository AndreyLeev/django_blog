import json

from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from .models import Post, Author, Comment
from .forms import CommentForm, PostForm, UserForm


def index(request):
    return render(request, 'index.html')


class AuthorsListView(generic.ListView):

    model = Author
    template_name = 'blog/bloggers_list.html'
    context_object_name = 'bloggers_list'
    paginate_by = 5
    

class PostsListView(generic.ListView):

    model = Post
    template_name = 'blog/posts_list.html'
    context_object_name = 'newest_post_list'
    paginate_by = 5


class PostView(generic.DetailView):

    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class BlogerView(generic.DetailView):

    model = Author
    template_name = 'blog/blogger_detail.html'
    context_object_name = 'blogger'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newest_post_list'] = Post.objects.filter(author=kwargs.get('object'))
        return context


class CommentsListView(generic.ListView):

    model = Comment
    template_name = 'blog/comments_list.html'
    context_object_name = 'comments_list'

    def dispatch(self, request, *args, **kwargs):
        self.post_pk = kwargs.get('pk')
        return super(CommentsListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Comment.objects.filter(post__id=self.post_pk)
        return queryset


@login_required
def comment_create(request, pk):

    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form_content = form.cleaned_data.get('content')
            comment = Comment(
                content=form_content,
                author=request.user,
                post=post,
            )
            comment.save()
            return HttpResponseRedirect(
                reverse('blog:post', kwargs={"pk": post.id}),
            )
    

def user_sign_up(request):

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            bio = form.cleaned_data.get('bio')
            user = User.objects.create_user(username=username, password=raw_password)
            user.save()
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            author = Author(
                user=user,
                bio=bio,
            )
            author.save()
            return HttpResponseRedirect(reverse('blog:index'))
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'user_sign_up.html', context)


@login_required
def post_create(request):

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            author = Author.objects.filter(user=request.user)[0]
            post = Post(
                title=title,
                content=content,
                author=author,
            )
            post.save()
            return HttpResponseRedirect(reverse('blog:post', kwargs={"pk": post.id}))
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'blog/post_create.html', context)


