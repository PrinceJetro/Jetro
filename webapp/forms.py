# forms.py
from django import forms
from .models import *
 


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = [ 'content',]


class NewPostForm(forms.ModelForm):
    class Meta:
        model = NewPost
        fields = ['content']
class ImageForm(forms.ModelForm):
    class Meta:
        model = NewPost
        fields = ['image']

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = NewComments
        fields = [ 'content',]


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['image']
