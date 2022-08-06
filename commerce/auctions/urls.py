from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("<int:listing_id>/bid", views.bid, name="bid"),
    path("<int:listing_id>/comment", views.comment, name="comment"),
    path("<int:listing_id>/watch", views.watch, name="watch"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:listing_id>/unwatch", views.unwatch, name="unwatch"),
    path("categories", views.categories, name="categories"),
    path("categories/new_category", views.new_category, name="new_category"),
    path("categories/<int:category_id>", views.category, name="category"),
    path("categories/add_item/<int:listing_id>", views.add_to_category, name="add_to_category"),
    path("categories/remove_item/<int:listing_id>", views.remove_from_category, name="remove_from_category"),
]
