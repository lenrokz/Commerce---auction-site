from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("<int:listing_id>", views.listing_page, name="listing_page"),
    path("watchlist", views.watchlist_page, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category_listing/<str:category>", views.category_listings, name="category_listings")
]
