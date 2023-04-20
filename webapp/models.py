from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    def comment_count(self):
        return self.comments.count()
    
    def __str__(self):
        return self.title
    def is_liked_by(self, user):
        return self.likes.filter(id=user.id).exists()

class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.author} commented on {self.post}'


class NewPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField()
    image_link = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='New_post_likes', blank=True)

    def comment_count(self):
        return self.comments.count()
    
    def __str__(self):
        return self.title
    def is_liked_by(self, user):
        return self.likes.filter(id=user.id).exists()


class NewComments(models.Model):
    post = models.ForeignKey(NewPost, on_delete=models.CASCADE, related_name='newcomments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.author} commented on {self.post}'
