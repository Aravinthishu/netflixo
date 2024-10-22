from .models import Profile
from movie.models import Wishlist, Download, WatchHistory
from subscription.models import UserSubscription, SubscriptionPlan
from django.utils import timezone

def profile(request):
    profile_image = None
    profile_instance = None

    if request.user.is_authenticated:
        try:
            profile_instance = Profile.objects.get(user=request.user)
            profile_image = profile_instance.avatar  # Accessing the avatar property
        except Profile.DoesNotExist:
            # Handle case where profile doesn't exist
            profile_image = None

    return {'profile': profile_instance, 'profile_image': profile_image}

def wishlist_count(request):
    wishlist_items = 0
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user).count()
    return {'wishlist_items_count': wishlist_items}

def download_count(request):
    download_items = 0
    if request.user.is_authenticated:
        download_items = Download.objects.filter(user=request.user).count()
    return {'download_items_count': download_items}

def watch_movie_count(request):
    watch_movie_items = 0
    if request.user.is_authenticated:
        now = timezone.now()
        watch_movie_items = WatchHistory.objects.filter(
            user=request.user,
            watched_on__year=now.year,
            watched_on__month=now.month
        ).count()
    return {'watch_movie_items_count': watch_movie_items}

def is_subsciption(request):
    if request.user.is_authenticated:
        user = request.user
        subscription = UserSubscription.objects.filter(user=user).first()
        if subscription:
            end_date = subscription.end_date
            context = {
                'is_subscribed': True,
                'subscription':subscription,
            }
            return context
    return {'is_subscribed': False}