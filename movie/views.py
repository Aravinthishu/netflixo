from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import *
from django.db.models import Q
import os
from django.http import HttpResponse, Http404
from django.conf import settings
from django.utils import timezone
from django.contrib.postgres.search import TrigramSimilarity
# Create your views here.



def movie_view(request, id):
    movie = Movie.objects.get(id=id)
    context = {
        'movie': movie
    }
    return render(request, 'movie/movie_view.html', context)

def watch_movie(request, id):
    movie = Movie.objects.get(id=id)
    context = {
        'movie': movie
    }
    return render(request, 'movie/watch_movie.html', context)

def cast_view(request, id):
    cast = Cast.objects.get(id=id)  # Get the cast member by ID
    movie_list = Movie.objects.filter(Q(cast=cast) | Q(director=cast)).distinct()  
    print(movie_list)
    context = {
        'cast': cast,
        'movies': movie_list,  # Pass the list of movies to the context
    }
    return render(request, 'movie/cast_view.html', context)


from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

def add_to_wishlist(user, movie):
    wishlist_item, created = Wishlist.objects.get_or_create(user=user, movie=movie)
    return created  # Returns True if the item was created, False if it already existed


def remove_from_wishlist(user, movie):
    try:
        wishlist_item = Wishlist.objects.get(user=user, movie=movie)
        wishlist_item.delete()
        return True  # Successfully removed
    except Wishlist.DoesNotExist:
        return False  # Item not found in the wishlist


@login_required
def add_to_wishlist_view(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    added = add_to_wishlist(request.user, movie)
    if added:
        messages.success(request, "Movie is Add to the favourites")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.warning(request, "Movie is Already in favourites")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def remove_from_wishlist_view(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    removed = remove_from_wishlist(request.user, movie)
    if removed:
        messages.success(request, "Movie successfully removed from your favourites")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse("Movie was not in your wishlist.")

def download_movie(user, movie):
    download_item, created = Download.objects.get_or_create(user=user, movie=movie)
    return created  # Returns True if the item was created, False if it already existed

@login_required
def download_view(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    # Check if the movie is newly downloaded or already in downloads
    is_new_download = download_movie(request.user, movie)
    
    if is_new_download:
        messages.success(request, "Movie has been added to your downloads!")
    else:
        messages.info(request, "You have already downloaded this movie.")
    
    # Serve the file for download
    file_path = os.path.join(settings.MEDIA_ROOT, movie.image.path)
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/force-download')
            response['Content-Disposition'] = f'attachment; filename="{movie.image.name}"'
            return response
    else:
        raise Http404("Image not found")
    
@login_required
def watch_movie_view(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    # Get the existing watch history or create a new one if it doesn't exist
    watch_history, created = WatchHistory.objects.get_or_create(user=request.user, movie=movie)

    if not created:
        # If the movie has been watched before, update the 'watched_on' timestamp
        watch_history.watched_on = timezone.now()
        watch_history.save()
        messages.warning(request, f"You have re-watched {movie.name}. The watch time has been updated.")
    else:
        messages.success(request, f"You are watching {movie.name} for the first time.")
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def search_movies(request):
    query = request.GET.get('query', '')  # Get the search term from the form input
    if query:
        # Search for movies containing the query in their title, description, genre, or cast
        filtered_movies = (
            Movie.objects.filter(name__icontains=query) |  # Search by title
            Movie.objects.filter(description__icontains=query) |  # Search by description
            Movie.objects.filter(genre__name__icontains=query) |  # Search by genre name
            Movie.objects.filter(cast__name__icontains=query) | # Search by cast name
            Movie.objects.filter(director__name__icontains=query)  # Search by cast name
        ).distinct()  # Ensure no duplicates
    else:
        filtered_movies = Movie.objects.none()  # Return an empty QuerySet if no query

    context = {
        'movies': filtered_movies,
        'query': query
    }
    print(filtered_movies)
    # Render the template and pass the list of matching movies
    return render(request, 'movie/search_result.html', context)


def movies_page(request):
    # Get query parameters for sorting and filtering
    year_range = request.GET.get('year_range', '')
    genre_id = request.GET.get('genre', '')
    rating_range = request.GET.get('rating_range', '')
    sort_by = request.GET.get('sort_by', '')  # Sorting parameter

    # Start with all movies
    movies = Movie.objects.all()

    # Filter by year range
    if year_range:
        if year_range == '2000-2005':
            movies = movies.filter(year__gte=2000, year__lte=2005)
        elif year_range == '2006-2011':
            movies = movies.filter(year__gte=2006, year__lte=2011)
        elif year_range == '2012-2018':
            movies = movies.filter(year__gte=2012, year__lte=2018)
        elif year_range == '2019-2024':
            movies = movies.filter(year__gte=2019, year__lte=2024)

    # Filter by genre
    if genre_id:
        movies = movies.filter(genre__id=genre_id)

    # Filter by rating range
    if rating_range:
        if rating_range == '1-4':
            movies = movies.filter(imdb_rating__gte=1, imdb_rating__lte=5)
        elif rating_range == '4-6':
            movies = movies.filter(imdb_rating__gte=1, imdb_rating__lte=5)
        elif rating_range == '6-8':
            movies = movies.filter(imdb_rating__gte=5, imdb_rating__lte=8)
        elif rating_range == '8-10':
            movies = movies.filter(imdb_rating__gte=8, imdb_rating__lte=10)

    # Sorting logic
    if sort_by:
        if sort_by == 'title_asc':
            movies = movies.order_by('title')  # Sort by title A-Z
        elif sort_by == 'title_desc':
            movies = movies.order_by('-title')  # Sort by title Z-A
        elif sort_by == 'year_asc':
            movies = movies.order_by('year')  # Sort by year ascending
        elif sort_by == 'year_desc':
            movies = movies.order_by('-year')  # Sort by year descending
        elif sort_by == 'imdb_rating_asc':
            movies = movies.order_by('imdb_rating')  # Sort by rating ascending
        elif sort_by == 'imdb_rating_desc':
            movies = movies.order_by('-imdb_rating')  # Sort by rating descending

    # Get all available genres for filtering options
    genres = Genre.objects.all()

    context = {
        'movies': movies,
        'genres': genres,
        'selected_year_range': year_range,
        'selected_genre': genre_id,
        'selected_rating_range': rating_range,
        'selected_sort_by': sort_by
    }

    return render(request, 'movie/movies_page.html', context)


