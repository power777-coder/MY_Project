from django.urls import path
from .views import home , upload_waste , marketplace , my_listings

urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload_waste, name='upload_waste'),
    path('marketplace/', marketplace, name='marketplace'),
    path('my-listings/', my_listings, name='my_listings'),

]
