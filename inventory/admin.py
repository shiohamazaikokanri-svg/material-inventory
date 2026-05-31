from django.contrib import admin

from .models import MaterialItem


@admin.register(MaterialItem)
class MaterialItemAdmin(admin.ModelAdmin):
    list_display = (
        "key",
        "maker",
        "material",
        "thickness",
        "width",
        "length",
        "quantity",
        "weight",
        "place",
    )
    list_filter = ("material", "thickness", "place", "maker")
    search_fields = ("key", "maker", "material", "place", "address")
