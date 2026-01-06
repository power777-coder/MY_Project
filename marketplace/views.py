from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from .forms import WasteForm
from .models import Waste

# Create your views here.
def home(request):
    latest_wastes = Waste.objects.filter(
        status='available'
    ).order_by('-created_at')[:4]

    return render(
        request,
        'index.html',
        {'latest_wastes': latest_wastes}
)

@login_required
def upload_waste(request):
    if request.method == 'POST':
        form = WasteForm(request.POST, request.FILES)
        if form.is_valid():
            waste = form.save(commit=False)
            waste.user = request.user
            waste.save()
            return redirect('home')
    else:
        form = WasteForm()

    return render(request, 'marketplace/upload_waste.html', {'form': form})

def marketplace(request):
    wastes = Waste.objects.filter(status='available').order_by('-created_at')
    return render(request, 'marketplace/marketplace.html', {'wastes': wastes})

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