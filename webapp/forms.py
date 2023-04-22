# forms.py
from django import forms
from .models import *
 


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Make a comment'}))
    
    class Meta:
        model = Comments
        fields = ['content',]


class NewPostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Make a Post'}))
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
