from django.contrib import admin
from .models import Waste

@admin.register(Waste)
class WasteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'waste_type',
        'user',
        'weight_kg',
        'status',
        'created_at',
    )
    list_filter = ('waste_type', 'status')
    search_fields = ('user__username', 'description')
