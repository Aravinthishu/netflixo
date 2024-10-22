from django.db import models
from movie.models import Movie
# Create your models here.


class HeroSection(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='hero_sections', blank=True, null=True)

    def __str__(self):
        return f"{self.movie}"  # Use self.choice to reference the ForeignKey field