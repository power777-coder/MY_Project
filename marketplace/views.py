from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import WasteForm
from .models import Waste
from .ml_pricing import predict_price


# Home page – latest listings
def home(request):
    latest_wastes = Waste.objects.filter(
        status='available'
    ).order_by('-created_at')[:4]

    return render(
        request,
        'index.html',
        {'latest_wastes': latest_wastes}
    )


# Upload waste + ML price prediction
@login_required
def upload_waste(request):
    if request.method == 'POST':
        form = WasteForm(request.POST, request.FILES)

        if form.is_valid():
            waste = form.save(commit=False)
            waste.user = request.user

            # 🔥 ML PRICE PREDICTION
            waste.predicted_price = predict_price(
                waste.waste_type,
                waste.weight_kg
            )

            # Initially final price = predicted price
            waste.final_price = waste.predicted_price

            waste.save()
            return redirect('home')

    else:
        form = WasteForm()

    return render(
        request,
        'marketplace/upload_waste.html',
        {'form': form}
    )


# Marketplace page
def marketplace(request):
    wastes = Waste.objects.filter(
        status='available'
    ).order_by('-created_at')

    return render(
        request,
        'marketplace/marketplace.html',
        {'wastes': wastes}
    )


# User's own listings
@login_required
def my_listings(request):
    wastes = Waste.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'marketplace/my_listings.html',
        {'wastes': wastes}
    )
