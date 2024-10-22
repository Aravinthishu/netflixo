from django.shortcuts import render, get_object_or_404, redirect
from .models import SubscriptionPlan, UserSubscription
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required  

def subscription_plans(request):
    user = request.user
    
    plan = SubscriptionPlan.objects.first()  # Only one plan
    return render(request, 'subscriptions/plans.html', {'plan': plan})

@login_required
def subscribe(request, duration):
    user = request.user
    plan = SubscriptionPlan.objects.first()  # Only one plan

    # Dummy payment success
    if request.method == 'POST':
        # Create or update the user's subscription
        subscription, created = UserSubscription.objects.get_or_create(user=user, plan=plan, defaults={
            'duration': duration,
            'start_date': timezone.now(),
        })
        if not created:
            subscription.duration = duration
            subscription.start_date = timezone.now()
            subscription.end_date = None  # Reset end date to recalculate
            user.is_premium_member = True
            subscription.save()
        messages.success(request, f"You have successfully Subcribed")
        return redirect('home')

    return render(request, 'subscriptions/subscribe.html', {'plan': plan, 'duration': duration})
