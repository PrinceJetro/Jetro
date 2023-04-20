from .views import *
from django.urls import path

urlpatterns = [

    path('', home, name='home'),
    path('register', register, name="register"),
    path('login', login, name="login"),
    path('feeds/<int:pk>/',feeds, name='feeds'),
    path('feeds/<int:pk>/create_post/',newPost, name='create_post'),
     path('create_post/', newPost, name='create_post'),
     path("logout",logout_request, name= "logout"),
    path('comment/<int:pk>/',create_comment, name='create_comment'),
    path('post/<int:post_id>/like/', like_post, name='like_post'),
    path('post/<int:post_id>/new_like_post/', new_like_post, name='new_like_post'),
    path('post/<int:pk>/',post_detail, name='post_detail'),
    path('my_posts/', my_posts, name='my_posts'),
      path('feeds/<int:pk>/my_posts',my_posts, name='my_posts'),
       path('feeds/<int:pk>/other_posts/', my_posts, name='other_posts'),
       path("new", newPost, name="new"),
       path("create_post/image", image, name="image"),
       path("new_create_comment/<int:pk>/", new_create_comment, name="new_create_comment")


]