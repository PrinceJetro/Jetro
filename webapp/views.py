from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, authenticate, logout #add thi
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from email.message import EmailMessage
import ssl
import smtplib
# Create your views here.
from supabase import StorageException


from .forms import *
 
# Create your views here.
 
 


# Python program to view
# for displaying images
# for i in User.objects.all():
#     print(i.username)
#     sender_email = 'adegbuyijephthah@gmail.com'
#     receiver_email = i.email
#     password= "nxafdqmnwypeyusr"
#     subject = "Introducing Our New Chat Web App!"
#     body = f"""
#     Hi {i.username}, 
#     I hope this email finds you well. This is Jetro, the developer of the Jetrostagram, reaching out to you with exciting news! I wanted to personally update you on our latest project and invite you to be a part of it.

# Introducing our new chat web application: ChatWave. As a valued user of our previous web app, I wanted to extend an exclusive invitation to join our growing community on this exciting new platform.
    
#     Our chat web app provides a seamless and interactive way to connect with others in real-time. Whether you're looking to chat with friends, collaborate with colleagues, or meet new people with shared interests, our chat web app has got you covered.

# You can access the chat web app by clicking the following link: https://prince-jetro-chat-app.vercel.app/

# I encourage you to explore the chat web app, start conversations, and make meaningful connections. Your FEEDBACKS and SUGGESTIONS are valuable to us as we continue to improve and enhance the platform.

# Thank you for being a part of our community. We look forward to seeing you on the chat web app!

# Best regards,

# Jetro
# Developer of Jetrostagram
#     """
#     em= EmailMessage()
#     em["From"] = sender_email
#     em["To"] = receiver_email
#     em["subject"] = subject
#     em.set_content(body)

#     context = ssl.create_default_context()
#     with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
#         smtp.login(sender_email, password)
#         smtp.sendmail(sender_email,receiver_email, em.as_string())
#     print("Email sent successfully!")






def register(request):

    if request.method == 'POST':
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        username = request.POST["username"]
        password1 = request.POST["psw"]
        password2 = request.POST["psw-repeat"]
        email = request.POST["email"]

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "UserName Taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken")
                return redirect('register')
            else:
                user = User.objects.create_user(username = username,first_name=first_name,last_name=last_name, email=email, password= password1 )
                user.save()
                auth.login(request, user)
        else:
            messages.info(request, "Password not matching")
            return redirect('register')
        return redirect("login")
    
    else:
        return  render(request, 'register.html')


def login(request):
    if request.user.is_authenticated:

        return redirect(reverse('feeds', kwargs={'pk': request.user.pk}))
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']


        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect(reverse('feeds', kwargs={'pk': request.user.pk}))
        else:
            print(" none")
            messages.info(request, "Invalid Credentials")
            return redirect('login')
    else:
        return render(request, "login.html")
    
    

def home(request):
        if request.user.is_authenticated:
            print("Authenticated")

            return redirect(reverse('feeds', kwargs={'pk': request.user.pk}))
        
        return  render(request, 'login.html')

@login_required
def feeds(request, pk):  
    import random
    latest_posts = Post.objects.order_by('-created_at')[:1000]
    Newlatest_posts = NewPost.objects.order_by('-created_at')[:1000]

    # Shuffle the posts randomly
    sto = Story.objects.order_by('-created_at')[:3]
    p = Post.objects.order_by('-created_at')[:100]
    new = NewPost.objects.order_by('-created_at')[:100]
    post = Comments.objects.order_by('-id')[:100]
    newcomment = NewComments.objects.order_by('-id')[:100]
    for i in Post.objects.all():
        post.title = i.author
    for j in NewPost.objects.all():
        post.title = i.author


    context = { 'p': latest_posts, 
               'post': post, 
               'pk': pk, 
               "new": Newlatest_posts, 
               'newcomment': newcomment,
               "sto":sto
            }

    return render(request, 'index.html', context )



from .models import Post
from .forms import PostForm


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse('feeds', kwargs={'pk': request.user.pk}))
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})



@login_required
def create_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  # Set the post to the current post
            comment.author = request.user  # Set the author to the current user
            comment.save()
            for c in post.comments.all():
                print(f"{c.author.username} commented on {c.post.title} by {c.post.author.username}")
            print(c.post.author.email)
            # set up the email parameters

#            sender_email = 'adegbuyijephthah@gmail.com'
 #           receiver_email = c.post.author.email
  #          password= "iqmidezpskhnpafv"
   #         subject = c.post.title
    #        body = f'{c.author.username} made a new comment on your post title {c.post.title} click https://jetrostagram.vercel.app to login and view it'
     #       em= EmailMessage()
      #      em["From"] = sender_email
       #     em["To"] = receiver_email
        #    em["subject"] = subject
         #   em.set_content(body)

          #  context = ssl.create_default_context()
           # with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            #    smtp.login(sender_email, password)
             #   smtp.sendmail(sender_email,receiver_email, em.as_string())
            #print("Email sent successfully!")




            return redirect('feeds', pk=post.pk)
    else:
        form = CommentForm()
        context = {
        'post': post,
        'comments': comments,
        'form': form
    }
    return render(request, 'comment.html', context)

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("login")



def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('feeds', pk=post.pk)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comments.objects.filter(post=post)
    return render(request, 'post_detail.html', {'post': post, 'comments': comments})


@login_required
def my_posts(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
        posts = Post.objects.filter(author=user).order_by('-created_at')
        newposts = NewPost.objects.filter(author=user).order_by('-created_at')
    else:
        newposts = NewPost.objects.filter(author=request.user).order_by('-created_at')
        posts = Post.objects.filter(author=request.user).order_by('-created_at')

    return render(request, 'my_post.html', {'posts': posts, 'newposts': newposts})

def view_user_posts(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    context = {
        'user': user,
        'posts': posts
    }
    return render(request, 'user_posts.html', context)





from webapp.storage import SupabaseStorage
url = ''
def image(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            storage = SupabaseStorage()
            post = 'jetrostagramposts/' + image.name
            try:
                filename = storage.save(post, image)
            except:
                return HttpResponse("Please upload another image, this image already exists")

            global url 
            url = storage.url(filename)
            print(url)
            values = (("first", redirect("register")), ("second", url))
            dicti = dict(values) 
            print(dicti["second"])
            return redirect("create_post/content")
    else:
        image = ImageForm()
        return render(request, 'create_post.html', {"image": image})

def newPost(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            print("pass commit = false")
            #post.image_link = url 
            global url
            post.author = request.user
            post.image_link = url
            print(post.author)
            print(post.image_link)
            post.save()
            
            url =''
            # do something with the URL, e.g. save it to a model or return it to the user
            return redirect(reverse('feeds', kwargs={'pk': request.user.pk}))
    else:
        slt = NewPostForm()
        form = NewPost.objects.all()
    return render(request, 'contents.html', {'form': form, "slt":slt,"url":url})


@login_required
def new_create_comment(request, pk):
    post = get_object_or_404(NewPost, pk=pk)
    comments = post.newcomments.all()
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  # Set the post to the current post
            comment.author = request.user  # Set the author to the current user
            comment.save()
            for c in post.newcomments.all():
                print(f"{c.author.username} commented on {c.post.title} by {c.post.author.username}")
            print(c.post.author.email)
            # set up the email parameters

#            sender_email = 'adegbuyijephthah@gmail.com'
 #           receiver_email = c.post.author.email
  #          password= "iqmidezpskhnpafv"
   #         subject = c.post.title
    #        body = f'{c.author.username} made a new comment on your post title {c.post.title} click https://jetrostagram.vercel.app to login and view it'
     #       em= EmailMessage()
      #      em["From"] = sender_email
       #     em["To"] = receiver_email
        #    em["subject"] = subject
         #   em.set_content(body)

          #  context = ssl.create_default_context()
           # with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            #    smtp.login(sender_email, password)
             #   smtp.sendmail(sender_email,receiver_email, em.as_string())
            #print("Email sent successfully!")




            return redirect('feeds', pk=post.pk)
    else:
        form = CommentForm()
        context = {
        'post': post,
        'comments': comments,
        'form': form
    }
    return render(request, 'comment.html', context)

def new_like_post(request, post_id):
    post = get_object_or_404(NewPost, id=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('feeds', pk=post.pk)


def all_comments(request):       
        newcomments = NewComments.objects.order_by('-created_at')
        comments = Comments.objects.order_by('-created_at')

        return render(request, 'hotel_image_form.html', {'comments': comments, 'newcomments': newcomments})


def StoryView(request):
    if request.method == "POST":
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            storage = SupabaseStorage()
            story = 'jetrostagramstory/' + image.name
            try:
                filename = storage.save(story, image)
            except Exception:   
                return HttpResponse("Please upload another image, this image has already been posted by you")
                

            url = storage.url(filename)
            print(url)
            values = (("first", redirect("register")), ("second", url))
            dicti = dict(values) 
            print(dicti["second"])
            new_story = Story.objects.create(image_link=url,author= request.user)
            return redirect(reverse('feeds', kwargs={'pk': request.user.pk}))
    else:
        image = StoryForm()
        return render(request, 'story.html', {"image": image})
    

def all_StoryView(request):
    story_image = Story.objects.order_by('-created_at')[:100]

    return render(request, "all_story.html", {"story_image": story_image})