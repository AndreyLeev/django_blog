from django import forms
from django.contrib.auth.forms import UserCreationForm


class CommentForm(forms.Form):

    content = forms.CharField(max_length=2000, widget=forms.Textarea)
    

class PostForm(forms.Form):
    
    title = forms.CharField(max_length=200)
    content = forms.CharField(max_length=2000, widget=forms.Textarea)


class UserForm(UserCreationForm):

    bio = forms.CharField(max_length=2000, widget=forms.Textarea)