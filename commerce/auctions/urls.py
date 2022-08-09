from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("add/", views.add, name="add"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watch/", views.watch, name="watch"),
    path("comment/", views.comment, name="comment"),
    path("account/", views.account, name="account"),
    path("bid/", views.bid, name="bid"),
    path("close/", views.close, name="close"),
    path("search/", views.search, name="search")
]
