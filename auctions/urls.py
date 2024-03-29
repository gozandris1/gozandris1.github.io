from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.createlisting, name="newlisting"),
    path("categories", views.categorypage, name="categories"),
    path("watchlist", views.whatchlistpage, name="watchlist"),
    path("<int:listing_id>", views.listingpage, name="listing")
]
