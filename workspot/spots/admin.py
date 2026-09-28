from django.contrib import admin

from .models import Spot


@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):
    list_display = ("number", "employee", "extra_info")
    search_fields = ("number",)
    list_filter = ("employee",)
