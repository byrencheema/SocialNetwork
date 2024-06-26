
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="create_post"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("follow/<str:username>/", views.toggle_follow, name="follow"),
    path("following", views.following, name="following"),
    path("edit/<int:post_id>/", views.edit_post, name="edit_post")
]
