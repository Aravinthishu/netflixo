from django.shortcuts import render
from django.contrib.auth.decorators import login_required  
from .models import Profile
from movie.models import Wishlist, Download
# Create your views here.

@login_required
def profile_view(request):
    try:
        # Use get() instead of filter() to get a single Profile object
        profile = Profile.objects.get(user=request.user)
        wishlist_items = Wishlist.objects.filter(user=request.user)
        download_items = Download.objects.filter(user=request.user)
    except Profile.DoesNotExist:
        profile = None
        print("Profile not found")

    context = {
        'profile': profile,
        'wishlist_items': wishlist_items,
        'download_items': download_items
    }
    return render(request, 'accounts/profile.html', context)
