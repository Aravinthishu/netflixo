from django.db import models
from django.contrib.auth.models import User
# Genre Model
class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Quality Model
class Quality(models.Model):
    quality_type = models.CharField(max_length=50)  # e.g., 720p, 1080p, 4K, etc.

    def __str__(self):
        return self.quality_type

# Language Model
class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Cast Model
class Cast(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cast/', null=True, blank=True)

    def __str__(self):
        return self.name

# Movie Model
class Movie(models.Model):
    name = models.CharField(max_length=200)
    title_logo = models.ImageField(upload_to='title_logo/', null=True, blank=True)
    image = models.ImageField(upload_to='movies/', null=True, blank=True)
    trailer = models.URLField(max_length=500, null=True, blank=True) 
    genre = models.ManyToManyField('Genre')  # No on_delete for ManyToManyField
    quality = models.ManyToManyField('Quality')  # No on_delete for ManyToManyField
    year = models.PositiveIntegerField()
    duration = models.DurationField()  # Stores time duration, e.g., 2:30:00
    description = models.TextField()
    language = models.ManyToManyField('Language')  # No on_delete for ManyToManyField
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1)  # e.g., 8.5
    cast = models.ManyToManyField('Cast', related_name='movies')  # No on_delete for ManyToManyField
    director = models.ForeignKey(Cast, on_delete=models.CASCADE, blank=True, null=True)
    is_premium = models.BooleanField(default=False)

    def formatted_duration(self):
        total_seconds = int(self.duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{hours}hr {minutes} mins"

    def __str__(self):
        return self.name

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the movie was added

    class Meta:
        unique_together = ('user', 'movie')  # Ensure each user can only have one entry for each movie

    def __str__(self):
        return f"{self.user.username} - {self.movie.name}"
    
class Download(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the movie was added

    class Meta:
        unique_together = ('user', 'movie')  # Ensure each user can only have one entry for each movie

    def __str__(self):
        return f"{self.user.username} - {self.movie.name}"
    
class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watched_on = models.DateTimeField(auto_now_add=True)  # Track when the movie was watched

    def __str__(self):
        return f"{self.user.username} - {self.movie.name}"