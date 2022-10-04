from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("addtowatchlist/<int:listing_id>", views.addtowatchlist, name="addtowatchlist"),
    path("categories", views.categories, name="categories")
]
