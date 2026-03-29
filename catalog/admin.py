from django.contrib import admin
from catalog.models import Place

@admin.register(Place)


class PlaceAdmin(admin.ModelAdmin):
    list_display = ["title",]