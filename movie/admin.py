from django.contrib import admin
from .models import *

# Inline for Genre
class GenreInline(admin.TabularInline):
    model = Movie.genre.through  # Accesses the intermediate table for the ManyToManyField
    extra = 1

# Inline for Quality
class QualityInline(admin.TabularInline):
    model = Movie.quality.through
    extra = 1

# Inline for Language
class LanguageInline(admin.TabularInline):
    model = Movie.language.through
    extra = 1

# Inline for Cast (to manage cast members)
class CastInline(admin.TabularInline):
    model = Movie.cast.through
    extra = 2  # Default number of cast members to add

# Movie Admin
class MovieAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'duration', 'imdb_rating', 'trailer')
    list_filter = ('year', 'genre', 'quality', 'language')
    search_fields = ('name', 'description')
    
    # Enable autocomplete for the director field
    autocomplete_fields = ['director', 'cast']  # This enables the search feature for director

    # Fieldsets to organize the movie details
    fieldsets = (
        ('Movie Details', {
            'fields': ('name', 'image', 'title_logo', 'description', 'year', 'duration', 'director', 'cast', 'imdb_rating', 'trailer')
        }),
        ('Additional Info', {
            'fields': ('genre', 'quality', 'language', 'is_premium')
        }),
    )

    # Inlines for displaying related models on the same page
    inlines = [GenreInline, QualityInline, LanguageInline, CastInline]

    # Ensure the ManyToMany relations save properly
    def save_model(self, request, obj, form, change):
        obj.save()
        form.save_m2m()

# Registering Models in the Admin
admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre)
admin.site.register(Quality)
admin.site.register(Language)
admin.site.register(Wishlist)
admin.site.register(Download)

# Cast Admin
class CastAdmin(admin.ModelAdmin):
    search_fields = ('name',)  # Allow searching by cast name
    list_display = ('name',)  # Display the name of the cast member
    list_filter = ('name',)  # Optional: Add filtering by cast name

# Registering Cast with its admin class
admin.site.register(Cast, CastAdmin)

# Customize the WatchHistory model admin
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'watched_on')  # Display these fields in the admin list
    search_fields = ('user__username', 'movie__title')  # Add search functionality for user and movie
    list_filter = ('watched_on', 'movie')  # Add filters for watched_on and movie

# Register models to admin site

admin.site.register(WatchHistory, WatchHistoryAdmin)