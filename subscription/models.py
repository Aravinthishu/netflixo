from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Subscription Plan with options for Monthly, Yearly, and 2-Year durations
class SubscriptionPlan(models.Model):
    DURATION_CHOICES = [
        ('M', 'Monthly'),
        ('Y', 'Yearly'),
        ('2Y', '2 Years'),
    ]
    
    name = models.CharField(max_length=100, default='Premium Plan')
    price_monthly = models.DecimalField(max_digits=6, decimal_places=2, default=10.00)
    price_yearly = models.DecimalField(max_digits=6, decimal_places=2, default=100.00)
    price_two_years = models.DecimalField(max_digits=6, decimal_places=2, default=180.00)

    def __str__(self):
        return self.name

# User subscription model
class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    duration = models.CharField(max_length=2, choices=SubscriptionPlan.DURATION_CHOICES, default='M')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()

    def is_active(self):
        return self.end_date > timezone.now()

    def __str__(self):
        return f"{self.user.username} - {self.get_duration_display()}"

    # Method to calculate the end date based on selected plan duration
    def calculate_end_date(self):
        if self.duration == 'M':  # Monthly plan
            return self.start_date + timedelta(days=30)
        elif self.duration == 'Y':  # Yearly plan
            return self.start_date + timedelta(days=365)
        elif self.duration == '2Y':  # 2 years plan
            return self.start_date + timedelta(days=730)

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.calculate_end_date()
        super(UserSubscription, self).save(*args, **kwargs)
