from django.contrib import admin

from .models import AutoOrder


@admin.register(AutoOrder)
class AutoOrderAdmin(admin.ModelAdmin):
    list_display = ("id",)
