from django.contrib import admin
from .models import Restaurant

# Register your models here.


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "rating",
        "name",
        "site",
        "email",
    )
    list_filter = ("rating", )
