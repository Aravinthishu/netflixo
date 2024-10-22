from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
    path('<int:id>', movie_view, name="movie_view" ),
    path('watch-movie/<int:id>', watch_movie, name="watch-movie" ),
    path('cast/<int:id>', cast_view, name="cast"),
    path('favouritesv/add/<int:movie_id>/', add_to_wishlist_view, name='add_to_wishlist'),
    path('favourites/remove/<int:movie_id>/', remove_from_wishlist_view, name='remove_from_wishlist'),
    path('download/<int:movie_id>/', download_view, name='download-movie'),
    path('movie-watching/<int:movie_id>', watch_movie_view, name="movie-watching"),
    path('search/', search_movies, name='search_movies'),
    path('movies/', movies_page, name='movies-page'),

]

