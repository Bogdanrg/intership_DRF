from django.contrib import admin

from .models import TradingUser


@admin.register(TradingUser)
class TradingUserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "username", "role", "balance")
    list_display_links = ("id",)
