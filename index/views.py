from django.shortcuts import render
from .models import HeroSection
from movie.models import Movie
# Create your views here.

def index(request):
    hero_section = HeroSection.objects.all()
    latest_movies = Movie.objects.order_by('-year')[:10]
    top_rated = Movie.objects.order_by('-imdb_rating')[:10]
    context = {
        'hero_section': hero_section,
        'latest_movies' : latest_movies,
        'top_rated' : top_rated,
    }
    return render(request, 'index/index.html', context)
