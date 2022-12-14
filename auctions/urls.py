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
    path("removefromwatchlist/<int:listing_id>", views.removefromwatchlist, name="removefromwatchlist"),
    path("categories", views.categories, name="categories"),
    path("categorypage/<str:cat>", views.categorypage, name="categorypage"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("close/<int:listing_id>", views.close, name="close")
]
