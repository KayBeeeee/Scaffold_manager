from django.contrib import admin
from .models import ScaffoldComponent

@admin.register(ScaffoldComponent)
class ScaffoldComponentAdmin(admin.ModelAdmin):
    list_display = ("asset_code", "name", "category", "length_mm", "weight_kg", "condition", "site", "next_inspection", "is_in_use")
    search_fields = ("asset_code", "name")
    list_filter = ("site", "condition", "category", "is_in_use")
