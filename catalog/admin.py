from django.contrib import admin
from catalog.models import Place, Image
from django.utils.html import format_html
from adminsortable2.admin import SortableTabularInline, SortableAdminBase
    

def show_image(obj):
     return format_html(
        '<img src="{}" style="max-width:300px; max-height=200px;">', 
        obj.image.url
    )


class ImageInline(SortableTabularInline):
    list_display = ["place",]
    model = Image
    extra = 0
    fields = (("image", show_image))
    readonly_fields = [show_image, ]
    
    
@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ["title",]
    inlines = [
        ImageInline,
    ]

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["place",]
    raw_id_fields = ["place",]
    readonly_fields = [show_image, ]
