from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator


from .models import User, Post


def index(request):
    postData = Post.objects.all()

    # Paginate the posts
    paginator = Paginator(postData, 5)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "posts": postData,
        "page_obj": page_obj
    })

def toggle_follow(request, username):
    user = request.user
    followedUser = User.objects.get(username=username)

    if user in followedUser.followers.all():
        followedUser.followers.remove(user)
        user.following.remove(followedUser)
    else:
        followedUser.followers.add(user)
        user.following.add(followedUser)

    return HttpResponseRedirect(reverse("profile", args=(username,)))

def following(request):
    user = request.user
    following = user.following.all()
    followingPosts = Post.objects.filter(user__in=following)

    return render(request, "network/following.html", {
        "followingPosts": followingPosts
    })

def profile(request, username):
    userData = User.objects.get(username=username)
    userPosts = Post.objects.filter(user=userData)

    return render(request, "network/profile.html", { 
        'userData': userData,
        'userPosts': userPosts
        })

def post(request):
    if request.method == "POST":
        content = request.POST["content"]
        user = request.user
        post = Post(user=user, content=content)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/index.html")

def edit_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == "POST":
        post.content = request.POST["content"]
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/edit_post.html", {
            "post": post
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
