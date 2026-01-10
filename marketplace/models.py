from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Waste(models.Model):

    WASTE_TYPE_CHOICES = [
        ('plastic', 'Plastic'),
        ('paper', 'Paper'),
        ('metal', 'Metal'),
        ('glass', 'Glass'),
        ('organic', 'Organic'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='waste_items'
    )

    waste_type = models.CharField(
        max_length=20,
        choices=WASTE_TYPE_CHOICES
    )

    description = models.TextField()

    weight_kg = models.FloatField()
    
    image = CloudinaryField(
    'image',
    blank=True,
    null=True
    )


    predicted_price = models.FloatField(
        blank=True,
        null=True
    )

    final_price = models.FloatField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.waste_type} - {self.user.username}"
