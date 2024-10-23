from django.shortcuts import render
from django.contrib.auth.decorators import login_required  
from .models import Profile
from movie.models import Wishlist, Download
from django.contrib import messages
from django.http import HttpResponseRedirect
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

def profile_update(request):
    if request.method == 'POST':
        try:
            profile = Profile.objects.get(user=request.user)

            # Update the image if a new file is uploaded
            if request.FILES.get('profile'):
                profile.image = request.FILES.get('profile')
                print(f"New image uploaded: {profile.image.url}")  # Debug: Check if the image is updated

            # Update user details
            profile.user.username = request.POST.get('username')
            profile.phone = request.POST.get('phone')

            # Update email directly on the User model
            profile.user.email = request.POST.get('email')

            # Save the User model to update username and email
            profile.user.save()

            # Save the Profile model to update image and phone
            profile.save()
            
            messages.success(request, "Profile updated successfully")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        messages.error(request, "Invalid request method")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

