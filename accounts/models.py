from django.db import models
from django.contrib.auth.models import User

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
