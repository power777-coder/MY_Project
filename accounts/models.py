from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    user_type = models.CharField(
        max_length=10,
        choices=[('seller', 'Seller'), ('buyer', 'Buyer')],
        default='seller'
    )
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
    
class EmailOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)

    def __str__(self):
        return f"{self.email} - {self.otp}"
