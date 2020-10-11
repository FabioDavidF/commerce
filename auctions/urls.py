from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create_listing', views.createListing, name='create_listing'),
    path('listing/<int:id>', views.listing, name='listing_page'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('add-<int:listing>', views.addToWatchlist, name='add-watchlist')
]
