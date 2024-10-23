from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.conf import settings
from django.utils import timezone

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    is_premium_member = models.BooleanField(default=False)

    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static('images/avatar.jpg')
        return avatar

    @property
    def email(self): 
        return self.user.email

    def __str__(self):
        return str(self.user.username)